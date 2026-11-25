"""Read-only verification of R2 test evidence, then resumable document recovery.

Never run full pytest here. Never change the original failed reports.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile
import time
import traceback
import zipfile

from phase176_closeout import gate as original
from phase176_closeout.documents import DOCUMENT_BLOBS, render_full
from phase176_closeout_r1_test_scope_repair import repair
from phase176_closeout_r2 import gate as r2
from phase176_closeout_r2.documents import sections as r2_sections
from .documents import sections

ROOT = original.ROOT
HEAD = '7b4e071b735d8c309c2155c04c96869e7e774bdb'
PACKAGE = 'phase176_closeout_r3'
PASS = 'PASS_PHASE176_ACTIVE_SCOPE_CLOSED_WITH_HISTORICAL_GUARD_OPEN'
STDOUT = 'a85672383551328c0752687200efacf8ff2cd95bd46da5ba61f85ac5663846b9'
STDERR = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
SUMMARY = '3546 passed in 41.33s'
R2_PINS = {
    'phase176_closeout_r2/README.md': '3bf337d4b1b61d51fed6c633c2c81ac47c9ea640',
    'phase176_closeout_r2/__init__.py': '959261a7f300a6c377f11c6dc69d89d21e1208c3',
    'phase176_closeout_r2/documents.py': 'e50b27aa061d6862f3b871c335ba02af7ea617bc',
    'phase176_closeout_r2/gate.py': '6b525af46cf7de39ae30bd41c7eb4a840af39648',
    'phase176_closeout_r2/run.ps1': '8b17b22bcd4a9aa9fe10d72692092b764464d4ff',
    'phase176_closeout_r2/tests/test_gate.py': '5562150890f61fc0edafa6960573c23c8a1e689f',
}
EVIDENCE_NAMES = ('attempt.json', 'report.json', 'preflight.json', 'public_audit.json',
                  'full_pytest_stdout.txt', 'full_pytest_stderr.txt')


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def evidence_dir():
    return repair.evidence_root() / PACKAGE


def read_r2_evidence():
    return {name: (r2.evidence_dir() / name).read_bytes() for name in EVIDENCE_NAMES}


def validate_r2_evidence(raw, r1_info):
    """Validate the saved test result, source snapshot and all earlier evidence."""
    require(set(raw) == set(EVIDENCE_NAMES), 'R2_EVIDENCE_INVENTORY_CHANGED')
    report, attempt, preflight, public = (json.loads(raw[n]) for n in (
        'report.json', 'attempt.json', 'preflight.json', 'public_audit.json'))
    expected = {'gate': 'FAIL_PHASE176_CLOSEOUT_R2', 'head': HEAD,
                'full_pytest_exit': 0, 'passed': 3546, 'summary': SUMMARY,
                'stdout_sha256': STDOUT, 'stderr_sha256': STDERR,
                'phase176_formally_closed': False, 'first_failure_preserved': True,
                'r1_evidence_preserved': True, 'active_scope': 'tests/',
                'historical_source_guard': 'FOUR_KNOWN_FAILURES_NOT_RERUN_NOT_PASSING'}
    require(all(report.get(k) == v for k, v in expected.items()), 'R2_REPORT_MISMATCH')
    require(report.get('error', '').startswith('PermissionError(13,')
            and 'write_full_documents' in report.get('traceback', '')
            and 'PermissionError' in report['traceback'], 'R2_FAILURE_NOT_DOCUMENT_PERMISSION_ERROR')
    require(original.digest(raw['full_pytest_stdout.txt']) == STDOUT
            and original.digest(raw['full_pytest_stderr.txt']) == STDERR,
            'R2_FULL_PYTEST_HASH_MISMATCH')
    require(r2.parse_summary(raw['full_pytest_stdout.txt'].decode('utf-8'), 0) == (3546, SUMMARY),
            'R2_SUMMARY_MISMATCH')
    require(report.get('preflight') == preflight and report.get('public_audit') == public
            and preflight.get('head') == HEAD and preflight.get('r1') == r1_info
            and preflight.get('historical_tests') == list(original.HISTORICAL),
            'R2_SNAPSHOT_MISMATCH')
    require(attempt.get('head') == HEAD and tuple(attempt.get('command', [])[1:]) == r2.ACTIVE_COMMAND
            and attempt.get('first_failure_evidence') == r1_info['first_failure_evidence']
            and attempt.get('r1_evidence') == r1_info['r1_evidence'], 'R2_ATTEMPT_MISMATCH')
    original.verify_public(public)
    require(set(preflight['documents']) == set(DOCUMENT_BLOBS), 'R2_DOCUMENT_INVENTORY_CHANGED')
    for name, pin in DOCUMENT_BLOBS.items():
        require(preflight['documents'][name]['git_blob'] == pin, 'R2_DOCUMENT_PIN_CHANGED:' + name)
    return report


def verify_checkout():
    """Allow only the reviewed five document paths to differ from tested HEAD."""
    from phase175_r4r14r11_closeout_preflight.audit import KNOWN_LEGACY_FAILURES
    from phase176_r3r60r2_public_citation_premise_elision.apply import planned_changes
    git = original.git
    require(Path(os.fsdecode(git('rev-parse', '--show-toplevel').strip())).resolve() == ROOT.resolve(),
            'WRONG_REPOSITORY_ROOT')
    require(git('branch', '--show-current').strip() == b'develop', 'DEVELOP_BRANCH_REQUIRED')
    for ref in ('HEAD', 'origin/develop'):
        require(git('rev-parse', ref).decode('ascii').strip() == HEAD, 'UNREVIEWED_REF:' + ref)
    require(not git('diff', '--cached', '--name-only'), 'STAGED_CHANGES_REQUIRE_REVIEW')
    changed = set(os.fsdecode(git('diff', '--name-only', 'HEAD')).splitlines())
    require(changed <= set(DOCUMENT_BLOBS), 'UNREVIEWED_TRACKED_CHANGES:' + repr(sorted(changed)))
    require(tuple(KNOWN_LEGACY_FAILURES) == original.HISTORICAL
            and all((ROOT / n.split('::')[0]).is_file() for n in original.HISTORICAL),
            'HISTORICAL_GUARD_SCOPE_CHANGED')
    for name, pin in r2.SOURCE_PINS.items():
        require(git('rev-parse', 'HEAD:' + name).decode('ascii').strip() == pin
                and repair.same_blob((ROOT / name).read_bytes(), pin), 'SOURCE_PIN_CHANGED:' + name)
    for name, pin in R2_PINS.items():
        require(repair.same_blob((ROOT / name).read_bytes(), pin), 'R2_SOURCE_PIN_CHANGED:' + name)
    untracked = set(os.fsdecode(git('ls-files', '--others', '--exclude-standard')).splitlines())
    allowed = set(R2_PINS) | {PACKAGE + '/' + n for n in (
        '__init__.py', 'README.md', 'gate.py', 'documents.py', 'run.ps1', 'tests/test_gate.py')}
    require(untracked <= allowed, 'UNREVIEWED_UNTRACKED_FILES:' + repr(sorted(untracked - allowed)))
    require(all(raw == new for raw, new in planned_changes().values()), 'R60R2_NOT_APPLIED')
    info = r2.verify_r1_evidence()
    r2.verify_archive(info)
    return info


def choose_original(candidates, expected_sha, expected_bytes, pin):
    """Select only bytes matching the R2 preflight and the reviewed Git blob."""
    for raw in candidates:
        if (len(raw) == expected_bytes and original.digest(raw) == expected_sha
                and repair.same_blob(raw, pin)):
            return raw
    raise RuntimeError('ORIGINAL_BYTES_NOT_RECOVERABLE')


def classify(current, baseline, old_final, new_final):
    for name, raw in (('R3_FINAL', new_final), ('R2_FINAL', old_final), ('ORIGINAL', baseline)):
        if current == raw:
            return name
    raise RuntimeError('UNREVIEWED_DOCUMENT_CONTENT')


def document_plan(report, report_hash):
    """Reconstruct exact full files, even if R2 rollback stopped partway."""
    old_sections, new_sections = r2_sections(report), sections(report, report_hash)
    result = {}
    for name, pin in DOCUMENT_BLOBS.items():
        record = report['preflight']['documents'][name]
        require(original.git('rev-parse', 'HEAD:' + name).decode('ascii').strip() == pin,
                'DOCUMENT_GIT_BLOB_CHANGED:' + name)
        current = (ROOT / name).read_bytes()
        saved = r2.evidence_dir() / 'original_full' / name
        committed = original.git('show', HEAD + ':' + name)
        lf = committed.replace(b'\r\n', b'\n')
        candidates = [current]
        if saved.is_file():
            candidates.append(saved.read_bytes())
        candidates.extend((committed, lf, lf.replace(b'\n', b'\r\n')))
        try:
            baseline = choose_original(candidates, record['sha256'], record['bytes'], pin)
            previous = render_full(name, baseline, old_sections[name])
            updated = render_full(name, baseline, new_sections[name])
            state = classify(current, baseline, previous, updated)
        except (RuntimeError, ValueError) as exc:
            raise RuntimeError(str(exc) + ':' + name) from exc
        result[name] = {'original': baseline, 'r2': previous, 'final': updated,
                        'current': current, 'state': state}
    return result


def preflight():
    info = verify_checkout()
    raw = read_r2_evidence()
    report = validate_r2_evidence(raw, info)
    hashes = {n: original.digest(v) for n, v in raw.items()}
    return report, hashes, document_plan(report, hashes['report.json'])


def write_bundle(folder, plan):
    """Generate and verify complete copies outside the Dropbox checkout first."""
    for name, row in plan.items():
        for kind, key in (('original_full', 'original'), ('final_full', 'final')):
            path = folder / kind / name
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('xb') as stream:
                stream.write(row[key])
            require(path.read_bytes() == row[key], 'OUTPUT_MISMATCH:' + name)
    archive = folder / 'EHP_Phase176_Final_Five_Full_Documents.zip'
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as zf:
        for name, row in plan.items():
            zf.writestr(name, row['final'])
    with zipfile.ZipFile(archive) as zf:
        require(zf.testzip() is None and set(zf.namelist()) == set(plan)
                and all(zf.read(name) == row['final'] for name, row in plan.items()), 'FULL_ZIP_MISMATCH')
    return str(archive)


def replace_document(target, expected, updated):
    """Use an atomic same-directory replacement; never truncate the target."""
    require(target.read_bytes() == expected, 'CONCURRENT_DOCUMENT_CHANGE:' + str(target))
    if expected == updated:
        return
    fd, temporary = tempfile.mkstemp(prefix=target.name + '.phase176r3-', dir=target.parent)
    temp = Path(temporary)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(updated)
            stream.flush()
            os.fsync(stream.fileno())
        for i in range(3):
            require(target.read_bytes() == expected, 'CONCURRENT_DOCUMENT_CHANGE:' + str(target))
            try:
                os.replace(temp, target)
                break
            except PermissionError as exc:
                if i == 2:
                    raise PermissionError(13, 'DOCUMENT_LOCKED:' + str(target)) from exc
                time.sleep(0.25)
        require(target.read_bytes() == updated, 'APPLIED_DOCUMENT_MISMATCH:' + str(target))
    finally:
        if temp.exists():
            temp.unlink()


def apply_documents(plan):
    """Each document is atomic. Retain verified partial progress on a lock.

    Do not attempt a rollback against a possibly locked target. A new R3 attempt
    recognizes exactly its own output, R2 output, and the verified originals.
    """
    for name, row in plan.items():
        replace_document(ROOT / name, row['current'], row['final'])
        print('PHASE176_CLOSEOUT_R3_DOCUMENT_APPLIED=' + name, flush=True)
    require(all((ROOT / name).read_bytes() == row['final'] for name, row in plan.items()),
            'FINAL_DOCUMENT_MISMATCH')


def run(dry_run=False):
    root = evidence_dir()
    final_report = root / 'final_report.json'
    if final_report.exists():
        print('PHASE176_CLOSEOUT_R3_GATE=FAIL_EXISTING_FINAL_REPORT_REQUIRES_REVIEW')
        print('REPORT=' + str(final_report))
        return 1
    try:
        report, hashes, plan = preflight()
        states = {name: row['state'] for name, row in plan.items()}
        print('PHASE176_CLOSEOUT_R3_HEAD=' + HEAD)
        print('PHASE176_CLOSEOUT_R3_R2_FULL_PYTEST=' + SUMMARY)
        print('PHASE176_CLOSEOUT_R3_FULL_PYTEST_RERUN=NOT_RUN')
        print('PHASE176_CLOSEOUT_R3_DOCUMENT_STATES=' + json.dumps(states))
        print('PHASE176_CLOSEOUT_R3_R2_TRACEBACK_BEGIN')
        print(report['traceback'])
        print('PHASE176_CLOSEOUT_R3_R2_TRACEBACK_END')
        if dry_run:
            print('PHASE176_CLOSEOUT_R3_GATE=PASS_R3_READ_ONLY_DRYRUN')
            return 0
    except Exception as exc:
        print('PHASE176_CLOSEOUT_R3_GATE=FAIL_PREFLIGHT')
        print('PHASE176_CLOSEOUT_R3_ERROR=' + repr(exc))
        return 1
    root.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=root))
    original.store_json(folder / 'attempt.json', {'head': HEAD, 'started_utc': datetime.now(timezone.utc).isoformat(),
                        'r2_evidence_sha256': hashes, 'document_states': states, 'full_pytest_rerun': 'NOT_RUN'})
    result = {'gate': 'FAIL_PHASE176_CLOSEOUT_R3', 'phase176_formally_closed': False,
              'head': HEAD, 'full_pytest_rerun': 'NOT_RUN', 'full_pytest_exit': 0,
              'passed': 3546, 'summary': SUMMARY, 'stdout_sha256': STDOUT, 'stderr_sha256': STDERR,
              'r2_evidence_sha256': hashes, 'initial_document_states': states,
              'historical_source_guard': report['historical_source_guard']}
    try:
        result['archive'] = write_bundle(folder, plan)
        require({n: original.digest(v) for n, v in read_r2_evidence().items()} == hashes,
                'R2_EVIDENCE_CHANGED_BEFORE_APPLY')
        require(verify_checkout() == report['preflight']['r1'], 'CHECKOUT_CHANGED_BEFORE_APPLY')
        apply_documents(plan)
        require(verify_checkout() == report['preflight']['r1'], 'CHECKOUT_CHANGED_AFTER_APPLY')
        require({n: original.digest(v) for n, v in read_r2_evidence().items()} == hashes,
                'R2_EVIDENCE_CHANGED_AFTER_APPLY')
        require(set(os.fsdecode(original.git('diff', '--name-only', 'HEAD')).splitlines()) == set(DOCUMENT_BLOBS),
                'FINAL_TRACKED_DIFF_MISMATCH')
        original.git('diff', '--check')
        require(all((ROOT / name).read_bytes() == row['final'] for name, row in plan.items()),
                'FINAL_DOCUMENT_CHANGED')
        result.update(documents=[{'path': n, 'before_sha256': original.digest(row['original']),
                                  'after_sha256': original.digest(row['final']), 'full_bytes': len(row['final'])}
                                 for n, row in plan.items()],
                      r2_evidence_preserved=True, first_failure_preserved=True, r1_evidence_preserved=True,
                      public_audit=report['public_audit'], gate=PASS, phase176_formally_closed=True)
    except BaseException as exc:
        result.update(error=repr(exc), traceback=traceback.format_exc())
    result['completed_utc'] = datetime.now(timezone.utc).isoformat()
    path = folder / 'report.json'
    original.store_json(path, result)
    if result['phase176_formally_closed']:
        # The immutable R2 report is never overwritten; this is a separate final marker.
        with final_report.open('x', encoding='utf-8') as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
    for key in ('head', 'summary', 'full_pytest_rerun', 'archive', 'r2_evidence_preserved',
                'phase176_formally_closed', 'error', 'gate'):
        if key in result:
            print('PHASE176_CLOSEOUT_R3_' + key.upper() + '=' + json.dumps(result[key], ensure_ascii=False))
    print('REPORT=' + str(path))
    return 0 if result['phase176_formally_closed'] else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    return run(parser.parse_args().dry_run)


if __name__ == '__main__':
    raise SystemExit(main())

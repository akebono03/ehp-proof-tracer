"""One-shot Phase 176 gate; preserve evidence and publish full files only on PASS."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import traceback
import zipfile

from .documents import DOCUMENT_BLOBS, MARKER, render_full, sections

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
HEAD = '471d79109d3054b088c7f910372b5f4f6cd5efa1'
ACTIVE_COMMAND = ('-B', '-m', 'pytest', '-q', '--tb=short', '--disable-warnings', '-p', 'no:cacheprovider', 'tests')
HISTORICAL = (
    'phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_guard.py::test_checkout_protects_real_upstream_sources',
    'phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_guard.py::test_wrong_source_sha_is_rejected',
    'phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/tests/test_source_guard.py::test_checked_source_guard_after_install',
    'phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/tests/test_source_guard.py::test_import_and_full_function_emitted_from_actual_file',
)


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, check=True, capture_output=True).stdout


def evidence_dir():
    return Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE


def store_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def digest(raw):
    return sha256(raw).hexdigest()


def checkout_state():
    return (git('rev-parse', 'HEAD'), git('diff', '--binary', 'HEAD'),
            git('diff', '--cached', '--binary'), git('status', '--porcelain', '-z'))


def preflight():
    from phase176_r3r60r2_public_citation_premise_elision.apply import planned_changes
    from phase175_r4r14r11_closeout_preflight.audit import KNOWN_LEGACY_FAILURES
    if Path(os.fsdecode(git('rev-parse', '--show-toplevel').strip())).resolve() != ROOT.resolve():
        raise RuntimeError('WRONG_REPOSITORY_ROOT')
    if git('branch', '--show-current').strip() != b'develop':
        raise RuntimeError('DEVELOP_BRANCH_REQUIRED')
    head = git('rev-parse', 'HEAD').decode('ascii').strip()
    if head != HEAD or git('rev-parse', 'origin/develop').decode('ascii').strip() != HEAD:
        raise RuntimeError('UNREVIEWED_HEAD_OR_REMOTE_TRACKING_REF')
    if git('diff', '--name-only', 'HEAD') or git('diff', '--cached', '--name-only'):
        raise RuntimeError('TRACKED_CHANGES_REQUIRE_REVIEW')
    git('diff', '--check')
    if not (ROOT / 'tests' / 'conftest.py').is_file():
        raise RuntimeError('ACTIVE_TESTS_DIRECTORY_MISSING')
    if tuple(KNOWN_LEGACY_FAILURES) != HISTORICAL or not all((ROOT / n.split('::')[0]).is_file() for n in HISTORICAL):
        raise RuntimeError('HISTORICAL_GUARD_SCOPE_CHANGED')
    if any(raw != new for raw, new in planned_changes().values()):
        raise RuntimeError('R60R2_NOT_APPLIED')
    documents = {}
    for name, pin in DOCUMENT_BLOBS.items():
        if git('rev-parse', 'HEAD:' + name).decode('ascii').strip() != pin:
            raise RuntimeError('UNREVIEWED_DOCUMENT_BLOB:' + name)
        raw = (ROOT / name).read_bytes()
        if MARKER.encode() in raw or b'PHASE175_R4R14R14_FINAL_CLOSEOUT_20261119' not in raw:
            raise RuntimeError('DOCUMENT_BOUNDARY_CHANGED:' + name)
        # Check all insertion anchors now, without writing a false final status.
        render_full(name, raw, '<!-- ' + MARKER + ' -->\n')
        documents[name] = {'git_blob': pin, 'sha256': digest(raw), 'bytes': len(raw)}
    return {'head': head, 'documents': documents, 'active_scope': 'tests/',
            'historical_source_guard': 'FOUR_KNOWN_FAILURES_NOT_RERUN_NOT_PASSING',
            'historical_tests': list(HISTORICAL),
            'untracked_paths': os.fsdecode(git('ls-files', '--others', '--exclude-standard')).splitlines()}


def parse_summary(stdout, code):
    if code != 0:
        raise RuntimeError('FULL_PYTEST_NONZERO_EXIT:' + str(code))
    rows = [line.strip() for line in stdout.splitlines()
            if re.search(r'\b\d+ passed\b', line) and re.search(r'\bin\s+\d', line)]
    if len(rows) != 1 or re.search(r'\b\d+\s+(?:failed|errors?|skipped|deselected|xfailed|xpassed)\b', rows[0]):
        raise RuntimeError('FULL_PYTEST_NONPASS_OR_AMBIGUOUS_SUMMARY')
    count = int(re.search(r'\b(\d+) passed\b', rows[0]).group(1))
    # The previously closed active suite contained 3546 tests. Never accept a
    # silently reduced scope; a larger all-pass count is allowed and recorded.
    if count < 3546:
        raise RuntimeError('ACTIVE_TEST_COUNT_BELOW_PHASE175_BASELINE')
    return count, rows[0]


def verify_public(report):
    expected = {'gate': 'PASS_R3R60R2_PUBLIC_CITATION_PREMISE_ELISION_CONNECTED',
                'status': 'complete', 'web_key': 'generic-complete-proof',
                'proof_steps': 62, 'inference_steps': 51, 'given_steps': 11,
                'citation_count': 10, 'open_goals': [], 'body_rows_after': 18,
                'display_reference_count_after': 9, 'root_display_count': 1,
                'references_without_explicit_body_use': [], 'model_unchanged': True,
                'partial_render_unchanged': True, 'public_adapter_verified': True,
                'retained_reference_blocks_unchanged_except_display_numbers': True,
                'public_connection': 'APPLIED', 'new_math_rules': 0,
                'new_given_registrations': 0}
    for key, value in expected.items():
        if report.get(key) != value:
            raise RuntimeError('PUBLIC_INVARIANT_CHANGED:' + key)


def write_full_documents(report, folder):
    """Prepare backups and verified complete ZIP before applying five files."""
    additions = sections(report)
    originals, updated = {}, {}
    for name in DOCUMENT_BLOBS:
        raw = (ROOT / name).read_bytes()
        if digest(raw) != report['preflight']['documents'][name]['sha256']:
            raise RuntimeError('DOCUMENT_CHANGED_DURING_GATE:' + name)
        originals[name] = raw
        updated[name] = render_full(name, raw, additions[name])
        for kind, content in (('original_full', raw), ('final_full', updated[name])):
            path = folder / kind / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            if path.read_bytes() != content:
                raise RuntimeError('DOCUMENT_OUTPUT_MISMATCH:' + name)
    archive = folder / 'EHP_Phase176_Final_Five_Full_Documents.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for name, raw in updated.items():
            zf.writestr(name, raw)
    with zipfile.ZipFile(archive) as zf:
        if zf.testzip() is not None or set(zf.namelist()) != set(updated) or any(zf.read(n) != v for n,v in updated.items()):
            raise RuntimeError('FULL_DOCUMENT_ZIP_MISMATCH')
    applied = []
    def replace(name, content):
        target = ROOT / name
        fd, temporary = tempfile.mkstemp(prefix=target.name + '.phase176-', dir=target.parent)
        try:
            with os.fdopen(fd, 'wb') as out:
                out.write(content)
            os.replace(temporary, target)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
    try:
        for name, raw in updated.items():
            if (ROOT / name).read_bytes() != originals[name]:
                raise RuntimeError('CONCURRENT_DOCUMENT_CHANGE:' + name)
            replace(name, raw)
            applied.append(name)
        if any((ROOT / n).read_bytes() != v for n,v in updated.items()):
            raise RuntimeError('APPLIED_DOCUMENT_MISMATCH')
        if set(os.fsdecode(git('diff', '--name-only', 'HEAD')).splitlines()) != set(DOCUMENT_BLOBS):
            raise RuntimeError('UNEXPECTED_TRACKED_DIFF')
        git('diff', '--check')
        if git('diff', '--cached', '--name-only'):
            raise RuntimeError('INDEX_CHANGED')
    except BaseException:
        for name in reversed(applied):
            # Never overwrite an external edit made after our own write.
            if (ROOT / name).read_bytes() != updated[name]:
                raise RuntimeError('CONCURRENT_CHANGE_REQUIRES_MANUAL_REVIEW:' + name)
            replace(name, originals[name])
        raise
    return {'archive': str(archive), 'files': [
        {'path': name, 'before_sha256': digest(originals[name]),
         'after_sha256': digest(updated[name]), 'full_bytes': len(updated[name])}
        for name in DOCUMENT_BLOBS]}


def run(dry_run=False):
    folder = evidence_dir()
    attempt, result_path = folder / 'attempt.json', folder / 'report.json'
    if attempt.exists() or result_path.exists():
        print('PHASE176_CLOSEOUT_GATE=FAIL_EXISTING_ATTEMPT_REQUIRES_REVIEW')
        print('EVIDENCE=' + str(folder))
        return 1
    try:
        snapshot = preflight()
        if dry_run:
            print('PHASE176_CLOSEOUT_HEAD=' + snapshot['head'])
            print('PHASE176_CLOSEOUT_FULL_PYTEST=NOT_RUN')
            print('PHASE176_CLOSEOUT_GATE=PASS_READ_ONLY_DRYRUN')
            return 0
        original_state = checkout_state()
        from phase176_r3r60r2_public_citation_premise_elision.audit import observe
        public = observe()
        verify_public(public)
        if checkout_state() != original_state:
            raise RuntimeError('REPOSITORY_CHANGED_DURING_PUBLIC_AUDIT')
        folder.mkdir(parents=True, exist_ok=True)
        store_json(folder / 'preflight.json', snapshot)
        store_json(folder / 'public_audit.json', public)
        with attempt.open('x', encoding='utf-8') as out:
            json.dump({'head':snapshot['head'], 'command':[sys.executable,*ACTIVE_COMMAND],
                       'started_utc':datetime.now(timezone.utc).isoformat()},out,indent=2)
    except Exception as exc:
        print('PHASE176_CLOSEOUT_GATE=FAIL_PREFLIGHT')
        print('PHASE176_CLOSEOUT_ERROR=' + repr(exc))
        return 1
    stdout_path, stderr_path = folder / 'full_pytest_stdout.txt', folder / 'full_pytest_stderr.txt'
    report = {'gate':'FAIL_PHASE176_CLOSEOUT', 'phase176_formally_closed':False,
              'head':snapshot['head'], 'preflight':snapshot, 'public_audit':public,
              'active_scope':'tests/', 'historical_source_guard':snapshot['historical_source_guard'],
              'full_pytest_exit':None}
    try:
        print('PHASE176_CLOSEOUT_FULL_PYTEST=STARTED_ONE_PHASE_END_RUN', flush=True)
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1')
        with stdout_path.open('wb') as out, stderr_path.open('wb') as err:
            proc = subprocess.run([sys.executable,*ACTIVE_COMMAND],cwd=ROOT,env=env,stdout=out,stderr=err,check=False)
        report.update(full_pytest_exit=proc.returncode, stdout_sha256=digest(stdout_path.read_bytes()),
                      stderr_sha256=digest(stderr_path.read_bytes()))
        count, summary = parse_summary(stdout_path.read_text(encoding='utf-8',errors='replace'),proc.returncode)
        report.update(passed=count, summary=summary)
        if checkout_state() != original_state:
            raise RuntimeError('REPOSITORY_CHANGED_DURING_FULL_PYTEST')
        report['documents'] = write_full_documents(report, folder)
        report.update(gate='PASS_PHASE176_ACTIVE_SCOPE_CLOSED_WITH_HISTORICAL_GUARD_OPEN',
                      phase176_formally_closed=True)
    except BaseException as exc:
        report.update(error=repr(exc), traceback=traceback.format_exc())
        for name,path in (('stdout_sha256',stdout_path),('stderr_sha256',stderr_path)):
            if path.exists():
                report[name] = digest(path.read_bytes())
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    store_json(result_path,report)
    if stdout_path.exists():
        print('\n'.join(stdout_path.read_text(encoding='utf-8',errors='replace').splitlines()[-12:]))
    if stderr_path.exists() and stderr_path.stat().st_size:
        print('\n'.join(stderr_path.read_text(encoding='utf-8',errors='replace').splitlines()[-8:]))
    for key in ('head','full_pytest_exit','passed','summary','stdout_sha256','stderr_sha256','historical_source_guard','phase176_formally_closed','error','documents','gate'):
        if key in report:
            print('PHASE176_CLOSEOUT_'+key.upper()+'='+json.dumps(report[key],ensure_ascii=False))
    print('REPORT='+str(result_path))
    return 0 if report['phase176_formally_closed'] else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    return run(parser.parse_args().dry_run)


if __name__ == '__main__':
    raise SystemExit(main())

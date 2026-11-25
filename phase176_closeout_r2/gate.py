"""One explicit retry after R1; never overwrite the original failed attempt."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback
from unittest.mock import patch

from phase176_closeout import gate as original
from phase176_closeout_r1_test_scope_repair import repair
from .documents import sections

ROOT = original.ROOT
HEAD = '7b4e071b735d8c309c2155c04c96869e7e774bdb'
PACKAGE = 'phase176_closeout_r2'
ACTIVE_COMMAND = original.ACTIVE_COMMAND
SOURCE_PINS = {
    'phase176_closeout/gate.py': 'b6f055a144e0c1b053d01b2ed9ccd4ef7ea90f35',
    'phase176_closeout/documents.py': '5c658a390c1758fda9796efd0fc714792116d5f9',
    'phase176_closeout_r1_test_scope_repair/repair.py': 'b2b3f3faa7cc113a1a5f8435b7b7a103054c1406',
    'phase176_closeout_r1_test_scope_repair/tests/test_repair.py': '3837ac286f1f0f55a48bb0f20c206e6f293efd31',
    **repair.CANONICAL,
}


def evidence_dir():
    return repair.evidence_root() / PACKAGE


def verify_r1_evidence():
    first = repair.failed_evidence()
    folder = repair.evidence_root() / repair.PACKAGE
    names = ('attempt.json', 'report.json', 'collect_stdout.txt', 'collect_stderr.txt')
    raw = {name: (folder / name).read_bytes() for name in names}
    report = json.loads(raw['report.json'])
    attempt = json.loads(raw['attempt.json'])
    expected = {'gate': 'PASS_PHASE176_CLOSEOUT_R1_ACTIVE_COLLECTION_RESTORED',
                'collection_exit': 0, 'collection_count': 3546, 'first_failure_preserved': True,
                'baseline_inventory_restored': True, 'full_pytest': 'NOT_RUN',
                'phase176_formally_closed': False}
    if any(report.get(k) != v for k, v in expected.items()):
        raise RuntimeError('R1_REPORT_NOT_VERIFIED')
    pre = report['preflight']
    if (pre != attempt['preflight'] or pre['head'] != repair.HEAD
            or pre['first_failure_evidence'] != first
            or report['stdout_sha256'] != repair.sha(raw['collect_stdout.txt'])
            or report['stderr_sha256'] != repair.sha(raw['collect_stderr.txt'])):
        raise RuntimeError('R1_EVIDENCE_MISMATCH')
    if repair.parse_collection(raw['collect_stdout.txt'].decode('utf-8'), 0) != (3546, report['summary']):
        raise RuntimeError('R1_COLLECTION_SUMMARY_MISMATCH')
    if set(report['archives']) != set(repair.PINS):
        raise RuntimeError('R1_ARCHIVE_INVENTORY_MISMATCH')
    return {'collection_count': 3546, 'summary': report['summary'],
            'first_failure_evidence': first, 'r1_evidence': {n: repair.sha(v) for n,v in raw.items()},
            'archives': report['archives']}


def verify_archive(info):
    if repair.paths_at(HEAD) != repair.paths_at(repair.BASE) or repair.actual_python_paths() != repair.paths_at(repair.BASE):
        raise RuntimeError('ACTIVE_PYTHON_INVENTORY_CHANGED')
    expected = {'D\t' + name for name in repair.PINS}
    observed = set(original.git('diff', '--no-renames', '--name-status', repair.HEAD, HEAD, '--', 'tests').decode('utf-8').splitlines())
    if observed != expected:
        raise RuntimeError('UNREVIEWED_TEST_TREE_DIFF:' + repr(observed))
    for name, pin in repair.PINS.items():
        path = repair.archive_path(name)
        record = info['archives'][name]
        relative = path.relative_to(ROOT).as_posix()
        raw = path.read_bytes()
        if ((ROOT / name).exists() or record['archive'] != relative
                or not repair.same_blob(raw, pin) or repair.sha(raw) != record['sha256']
                or len(raw) != record['bytes']):
            raise RuntimeError('ARCHIVE_NOT_PRESERVED:' + name)
        original.git('ls-files', '--error-unmatch', '--', relative)


def preflight():
    for name, pin in SOURCE_PINS.items():
        if (original.git('rev-parse', 'HEAD:' + name).decode('ascii').strip() != pin
                or not repair.same_blob((ROOT / name).read_bytes(), pin)):
            raise RuntimeError('SOURCE_PIN_CHANGED:' + name)
    # Reuse the original exact source and document checks at the new reviewed HEAD.
    # The original failure gate itself remains unchanged on disk.
    with patch.object(original, 'HEAD', HEAD):
        snapshot = original.preflight()
    info = verify_r1_evidence()
    verify_archive(info)
    snapshot['r1'] = info
    return snapshot


def parse_summary(stdout, code):
    count, summary = original.parse_summary(stdout, code)
    if count != 3546:
        raise RuntimeError('FINAL_COUNT_DIFFERS_FROM_R1_COLLECTION')
    return count, summary


def write_full_documents(report, folder):
    # Only the document text builder is replaced, within the original transactional writer.
    with patch.object(original, 'sections', sections):
        return original.write_full_documents(report, folder)


def run(dry_run=False):
    folder = evidence_dir()
    attempt, result_path = folder / 'attempt.json', folder / 'report.json'
    if attempt.exists() or result_path.exists():
        print('PHASE176_CLOSEOUT_R2_GATE=FAIL_EXISTING_ATTEMPT_REQUIRES_REVIEW')
        print('EVIDENCE=' + str(folder))
        return 1
    try:
        snapshot = preflight()
        if dry_run:
            print('PHASE176_CLOSEOUT_R2_HEAD=' + snapshot['head'])
            print('PHASE176_CLOSEOUT_R2_FULL_PYTEST=NOT_RUN')
            print('PHASE176_CLOSEOUT_R2_GATE=PASS_R2_READ_ONLY_DRYRUN')
            return 0
        state = original.checkout_state()
        from phase176_r3r60r2_public_citation_premise_elision.audit import observe
        public = observe()
        original.verify_public(public)
        if original.checkout_state() != state or preflight() != snapshot:
            raise RuntimeError('REPOSITORY_OR_EVIDENCE_CHANGED_DURING_PUBLIC_AUDIT')
        folder.mkdir(parents=True, exist_ok=True)
        with attempt.open('x', encoding='utf-8') as out:
            json.dump({'head': snapshot['head'], 'command': [sys.executable, *ACTIVE_COMMAND],
                       'started_utc': datetime.now(timezone.utc).isoformat(),
                       'first_failure_evidence': snapshot['r1']['first_failure_evidence'],
                       'r1_evidence': snapshot['r1']['r1_evidence']}, out, indent=2)
        original.store_json(folder / 'preflight.json', snapshot)
        original.store_json(folder / 'public_audit.json', public)
    except Exception as exc:
        print('PHASE176_CLOSEOUT_R2_GATE=FAIL_PREFLIGHT')
        print('PHASE176_CLOSEOUT_R2_ERROR=' + repr(exc))
        return 1
    stdout_path, stderr_path = folder / 'full_pytest_stdout.txt', folder / 'full_pytest_stderr.txt'
    report = {'gate': 'FAIL_PHASE176_CLOSEOUT_R2', 'phase176_formally_closed': False,
              'head': snapshot['head'], 'preflight': snapshot, 'public_audit': public,
              'active_scope': 'tests/', 'historical_source_guard': snapshot['historical_source_guard'],
              'full_pytest_exit': None}
    try:
        print('PHASE176_CLOSEOUT_R2_FULL_PYTEST=STARTED_ONE_REPAIRED_PHASE_END_RUN', flush=True)
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1')
        with stdout_path.open('xb') as out, stderr_path.open('xb') as err:
            proc = subprocess.run([sys.executable, *ACTIVE_COMMAND], cwd=ROOT, env=env, stdout=out, stderr=err, check=False)
        report.update(full_pytest_exit=proc.returncode, stdout_sha256=original.digest(stdout_path.read_bytes()),
                      stderr_sha256=original.digest(stderr_path.read_bytes()))
        count, summary = parse_summary(stdout_path.read_text(encoding='utf-8', errors='replace'), proc.returncode)
        report.update(passed=count, summary=summary)
        if original.checkout_state() != state or preflight() != snapshot:
            raise RuntimeError('REPOSITORY_OR_EVIDENCE_CHANGED_DURING_FULL_PYTEST')
        report['first_failure_preserved'] = True
        report['r1_evidence_preserved'] = True
        report['documents'] = write_full_documents(report, folder)
        report.update(gate='PASS_PHASE176_ACTIVE_SCOPE_CLOSED_WITH_HISTORICAL_GUARD_OPEN', phase176_formally_closed=True)
    except BaseException as exc:
        report.update(error=repr(exc), traceback=traceback.format_exc())
        for name, path in (('stdout_sha256', stdout_path), ('stderr_sha256', stderr_path)):
            if path.exists():
                report[name] = original.digest(path.read_bytes())
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    original.store_json(result_path, report)
    for path in (stdout_path, stderr_path):
        if path.exists():
            print('\n'.join(path.read_text(encoding='utf-8', errors='replace').splitlines()[-15:]))
    for key in ('head', 'full_pytest_exit', 'passed', 'summary', 'stdout_sha256', 'stderr_sha256',
                'first_failure_preserved', 'r1_evidence_preserved', 'historical_source_guard',
                'phase176_formally_closed', 'error', 'documents', 'gate'):
        if key in report:
            print('PHASE176_CLOSEOUT_R2_' + key.upper() + '=' + json.dumps(report[key], ensure_ascii=False))
    print('REPORT=' + str(result_path))
    return 0 if report['phase176_formally_closed'] else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    return run(parser.parse_args().dry_run)


if __name__ == '__main__':
    raise SystemExit(main())

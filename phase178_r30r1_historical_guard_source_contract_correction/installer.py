"""Install only the reviewed R4C test correction; rollback on a failed gate."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
HEAD = '77a263a440d811413796bd454787b71e64c27848'
TARGET = 'phase169_r4c_pi64_suspension_iso/tests/test_r4c_pi64_suspension_iso.py'
OLD_BLOB = '165bd5dee76978dd5d3f0cca40b4890f14b9257b'
NEW_SHA = '09455eeb686f5d97bb63a4cd8cc66f945c2b1446afd9dd9a5a698ba422049178'
GUARD = 'test_r4c_real_screened_iso_proof_has_three_prior_sources'
TESTS = (
    TARGET,
    'phase178_r20f1_historical_guard_audit/tests/test_audit.py',
    'phase178_r30_historical_guard_final_audit/tests/test_audit.py',
    'phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py',
    'phase178_r20r1_suspension_isomorphism_bridge_public/tests/test_public.py',
)


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def emit(key, value):
    print('PHASE178_R30R1_' + key + '=' + str(value), flush=True)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def gt(*args):
    return git(*args).decode('utf-8').strip()


def lf(raw):
    return raw.replace(b'\r\n', b'\n')


def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()


def validate_payload(old, new):
    require(blob(lf(old)) == OLD_BLOB, 'UNREVIEWED_ORIGINAL')
    require(hashlib.sha256(new).hexdigest() == NEW_SHA, 'PAYLOAD_HASH_CHANGED')
    before = {n.name: ast.dump(n) for n in ast.parse(lf(old)).body if isinstance(n, ast.FunctionDef)}
    after = {n.name: ast.dump(n) for n in ast.parse(new).body if isinstance(n, ast.FunctionDef)}
    require(before.keys() == after.keys(), 'FUNCTION_SET_CHANGED')
    require([k for k in before if before[k] != after[k]] == [GUARD], 'UNRELATED_FUNCTION_CHANGED')
    require(sum(k.startswith('test_') for k in after) == 6, 'LEGACY_TEST_COUNT_CHANGED')
    return new.replace(b'\n', b'\r\n') if b'\r\n' in old else new


def preflight():
    require(Path(gt('rev-parse', '--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    require(gt('branch', '--show-current') == 'develop', 'DEVELOP_REQUIRED')
    require(gt('rev-parse', 'HEAD') == gt('rev-parse', 'origin/develop') == HEAD, 'REVIEWED_HEAD_REQUIRED:' + HEAD)
    require(not git('status', '--porcelain', '--untracked-files=no'), 'TRACKED_WORKTREE_NOT_CLEAN')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    require(gt('rev-parse', 'HEAD:' + TARGET) == OLD_BLOB, 'ORIGINAL_BLOB_CHANGED')
    require(all((ROOT / p).is_file() for p in TESTS), 'FOCUSED_TEST_MISSING')
    old = (ROOT / TARGET).read_bytes()
    new = validate_payload(old, (PACKAGE / 'replacement.py.txt').read_bytes())
    return old, new


def validate_results(code, path):
    cases = list(ET.parse(path).getroot().iter('testcase'))
    require(code == 0 and len(cases) == 47, 'FOCUSED_EXIT_OR_COUNT_CHANGED')
    require(not any(c.find(tag) is not None for c in cases for tag in ('failure', 'error', 'skipped')), 'FOCUSED_FAILED_OR_SKIPPED')
    historical = [c for c in cases if 'test_r4c_pi64_suspension_iso' in c.get('classname', '')]
    require(len(historical) == 6 and len({c.get('name') for c in historical}) == 6
            and any(c.get('name') == GUARD for c in historical), 'HISTORICAL_TEST_SET_CHANGED')
    return len(cases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE.name
    base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))
    report = {'gate': 'FAIL_R30R1', 'dry_run': args.dry_run, 'full_pytest': 'NOT_RUN'}
    installed = False
    old = None
    try:
        old, new = preflight()
        emit('HEAD', HEAD)
        emit('TARGET', TARGET)
        emit('PAYLOAD_VERIFIED', 'YES')
        if args.dry_run:
            report['gate'] = 'PASS_R30R1_DRYRUN'
        else:
            (folder / 'original.py.txt').write_bytes(old)
            installed = True
            (ROOT / TARGET).write_bytes(new)
            require((ROOT / TARGET).read_bytes() == new, 'INSTALL_VERIFY_FAILED')
            require(gt('diff', '--name-only', 'HEAD').splitlines() == [TARGET], 'UNEXPECTED_TRACKED_CHANGE')
            git('diff', '--check')
            xml = folder / 'focused.xml'
            command = [sys.executable, '-B', '-m', 'pytest', '-q', '-s', '--import-mode=importlib', '-p', 'no:cacheprovider', '--junitxml=' + str(xml), *TESTS]
            report['command'] = command
            proc = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  encoding='utf-8', errors='replace', timeout=300)
            (folder / 'focused.txt').write_text(proc.stdout, encoding='utf-8')
            print(proc.stdout, flush=True)
            report['focused_count'] = validate_results(proc.returncode, xml)
            require('PHASE178_R30R1_HISTORICAL_REPLAY=VERIFIED' in proc.stdout
                    and 'PHASE178_R30R1_PRIOR_SOURCES=VERIFIED' in proc.stdout, 'REPLAY_MARKER_MISSING')
            require((ROOT / TARGET).read_bytes() == new and gt('diff', '--name-only', 'HEAD').splitlines() == [TARGET]
                    and gt('rev-parse', 'HEAD') == HEAD and not git('diff', '--cached', '--name-only'), 'POST_INSTALL_INTEGRITY_FAILED')
            git('diff', '--check')
            emit('HISTORICAL_GUARD', '6/6_PASS')
            emit('FOCUSED_TEST_COUNT', report['focused_count'])
            report['gate'] = 'PASS_R30R1_HISTORICAL_GUARD_CORRECTED'
    except BaseException as exc:
        report.update(error=repr(exc), traceback=traceback.format_exc())
        emit('ERROR', repr(exc))
        if installed and old is not None:
            # Restore only our own replacement, never overwrite a concurrent edit.
            if (ROOT / TARGET).read_bytes() == new:
                (ROOT / TARGET).write_bytes(old)
                emit('ROLLBACK', 'ORIGINAL_RESTORED')
            else:
                emit('ROLLBACK', 'MANUAL_REVIEW_REQUIRED')
    (folder / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    emit('REPORT', folder / 'report.json')
    emit('NEW_MATH_RULES', 0)
    emit('NEW_GIVEN', 0)
    emit('PROVIDER_CHANGED', 'NO')
    emit('RENDERER_CHANGED', 'NO')
    emit('FULL_PYTEST', 'NOT_RUN')
    emit('GATE', report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())

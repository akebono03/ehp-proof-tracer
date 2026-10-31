"""Phase 172 R3R1R1: guarded correction to read-only audit preflight only."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import os
from pathlib import Path
import subprocess
import sys

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / 'phase172_r3r1_hopf_chain_audit/audit.py'
CORRECTED = PACKAGE / 'corrected_audit_FULL.py'
ORIGINAL_SHA256 = 'dd7ce74dd6a367209a49349f2b6a95ff73496a6f1febcc51059abb4bc7555907'
CORRECTED_SHA256 = 'a5110955a0d98b9ec46663ce64bdedfba92938f254490a2c67d34baa67dbfad5'


def normalized(raw: bytes) -> bytes:
    source = raw.decode('utf-8-sig')
    if '\r' in source.replace('\r\n', ''):
        raise RuntimeError('mixed source newlines are unsupported')
    return source.replace('\r\n', '\n').encode('utf-8')


def sha256(raw: bytes) -> str:
    return hashlib.sha256(normalized(raw)).hexdigest()


def preflight() -> tuple[str, str, bytes, bytes]:
    result = subprocess.run(['git', 'branch', '--show-current'], cwd=ROOT,
                            capture_output=True, text=True, check=True)
    if result.stdout.strip() != 'develop':
        raise RuntimeError('correction requires develop; no files changed')
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout.strip()
    if not TARGET.is_file() or not CORRECTED.is_file():
        raise RuntimeError('R3R1 source or correction payload is missing')
    current = TARGET.read_bytes()
    replacement = CORRECTED.read_bytes()
    if sha256(replacement) != CORRECTED_SHA256:
        raise RuntimeError('bundled reviewed corrected source mismatch')
    current_sha = sha256(current)
    if current_sha not in (ORIGINAL_SHA256, CORRECTED_SHA256):
        raise RuntimeError('unreviewed R3R1 audit content; refusing replacement')
    return head, ('ALREADY_CORRECTED' if current_sha == CORRECTED_SHA256 else 'NEEDS_CORRECTION'), current, replacement


def command(args: list[str], report: Path, filename: str) -> None:
    env = os.environ.copy()
    env['PYTHONUTF8'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONPATH'] = str(ROOT) + os.pathsep + env.get('PYTHONPATH', '')
    run = subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                         encoding='utf-8', errors='replace', env=env, check=False)
    log = run.stdout + '\n' + run.stderr
    (report / filename).write_text(log, encoding='utf-8')
    print(log[-3000:], flush=True)
    if run.returncode:
        raise RuntimeError(f'command failed (exit {run.returncode}): {filename}')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--run-focused-tests', action='store_true')
    args = parser.parse_args()
    head, state, original, replacement = preflight()
    print('PHASE172_R3R1R1_BRANCH=develop', flush=True)
    print('PHASE172_R3R1R1_HEAD=' + head, flush=True)
    print('PHASE172_R3R1R1_PAYLOAD_GUARD=PASS', flush=True)
    print('PHASE172_R3R1R1_AUDIT_SOURCE_STATE=' + state, flush=True)
    if args.dry_run:
        print('PHASE172_R3R1R1_SOURCE_CHANGES=0', flush=True)
        print('PHASE172_R3R1R1_DRY_RUN=PASS', flush=True)
        return 0
    base = Path(os.environ.get('LOCALAPPDATA') or Path.home()) / 'EHPProofTracerRecovery'
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%fZ')
    report = base / ('phase172_r3r1r1_' + stamp)
    report.mkdir(parents=True, exist_ok=False)
    (report / 'audit.py.before').write_bytes(original)
    modified = state != 'ALREADY_CORRECTED'
    try:
        if modified:
            ending = b'\r\n' if b'\r\n' in original else b'\n'
            TARGET.write_bytes(normalized(replacement).replace(b'\n', ending))
        if sha256(TARGET.read_bytes()) != CORRECTED_SHA256:
            raise RuntimeError('post-write content mismatch')
        print('PHASE172_R3R1R1_AUDIT_GUARD_CORRECTED=PASS', flush=True)
        if args.run_focused_tests:
            command([sys.executable, '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider',
                     'phase172_r3r1r1_committed_renderer_guard_fix/tests/test_guard_fix.py'],
                    report, 'focused_guard.log')
            print('PHASE172_R3R1R1_GUARD_TESTS=PASS', flush=True)
        audit_args = [sys.executable, '-B', '-m', 'phase172_r3r1_hopf_chain_audit.audit']
        if args.run_focused_tests:
            audit_args.append('--run-focused-tests')
        command(audit_args, report, 'hopf_audit.log')
        print('PHASE172_R3R1R1_RESULT=PASS_CORRECTED_R3R1_AUDIT', flush=True)
        print('PHASE172_R3R1R1_REPORT=' + str(report), flush=True)
        return 0
    except Exception as error:
        if modified:
            TARGET.write_bytes(original)
            print('PHASE172_R3R1R1_RESTORED=PASS', flush=True)
        print('PHASE172_R3R1R1_RESULT=FAIL', flush=True)
        print('PHASE172_R3R1R1_REPORT=' + str(report), flush=True)
        print('PHASE172_R3R1R1_DIAGNOSTIC=' + repr(error), flush=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())

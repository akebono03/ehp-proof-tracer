"""Reviewed one-character Git blob SHA pin correction for R38."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
from pathlib import Path
import subprocess

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
R38 = ROOT / 'phase174_r3_r7_r38_source_bound_zero_image_public_wiring'
TARGET = R38 / 'install.py'
BASELINE = PACKAGE / 'baseline' / 'install.py'
REPLACEMENT = PACKAGE / 'replacement' / 'install.py'
BASE_HEAD = '660cadd928a2cbca00f71c5c35cd3af1230a54e9'
REVIEWED_R37_HEAD = '2e3fcfbea1a3816b146cf53320f9a3bbee618c52'
OLD_SHA256 = '4f5c908e11b8ba0e0c12aa07bad55ea79a51558d93433640c36d2816a7f8292b'
NEW_SHA256 = '8d4fae72b850bca241326759a59ee24aecb856158b25e62fbed44f42b9d539ef'
OLD_R9_BLOB = '2c44c68be90cb761d7bdd35e29f23977b5f93a2'
CORRECT_R9_BLOB = '2c44c68be90cb761d7bdd35e29f23977b5f93a2e'


def git(*args: str) -> str:
    return subprocess.run(('git',) + args, cwd=ROOT, check=True,
                          capture_output=True, text=True,
                          encoding='utf-8', errors='replace').stdout.strip()


def normalize(data: bytes) -> bytes:
    return data.replace(b'\r\n', b'\n')


def sha256_of(data: bytes) -> str:
    return hashlib.sha256(normalize(data)).hexdigest()


def verify_checkout() -> dict[str, object]:
    """Only reviewed HEADs and one exact R38 installer are accepted."""
    if Path(git('rev-parse', '--show-toplevel')).resolve() != ROOT.resolve():
        raise RuntimeError('Extract R38R1 into repository root')
    if git('branch', '--show-current') != 'develop':
        raise RuntimeError('R38R1 requires develop branch')
    local = git('rev-parse', 'HEAD')
    remote_text = git('ls-remote', 'origin', 'refs/heads/develop')
    remote = remote_text.split()[0] if remote_text else ''
    if remote != REVIEWED_R37_HEAD or local not in (BASE_HEAD, REVIEWED_R37_HEAD):
        raise RuntimeError('GitHub/local HEAD differs from reviewed R37 lineage')
    if git('diff', '--cached', '--name-only'):
        raise RuntimeError('Staged tracked changes require review')
    target_production = 'phase165_r6_2_unified_registry_r3_r4/context_provider_registry.py'
    tracked_changes = tuple(git('diff', '--name-only').splitlines())
    if tracked_changes not in ((), (target_production,)):
        raise RuntimeError('Unrelated tracked changes require review; nothing overwritten')
    for path in (TARGET, BASELINE, REPLACEMENT):
        if not path.is_file():
            raise RuntimeError('Required R38/R38R1 file is missing: ' + str(path))
    if sha256_of(BASELINE.read_bytes()) != OLD_SHA256:
        raise RuntimeError('R38R1 baseline content changed')
    if sha256_of(REPLACEMENT.read_bytes()) != NEW_SHA256:
        raise RuntimeError('R38R1 replacement content changed')
    old_text = normalize(BASELINE.read_bytes()).decode('utf8')
    new_text = normalize(REPLACEMENT.read_bytes()).decode('utf8')
    if (len(OLD_R9_BLOB) != 39 or len(CORRECT_R9_BLOB) != 40
            or old_text.count(OLD_R9_BLOB) != 1
            or new_text != old_text.replace(OLD_R9_BLOB, CORRECT_R9_BLOB)):
        raise RuntimeError('R38R1 altered code beyond the reviewed one-character SHA pin')
    previous = sha256_of(TARGET.read_bytes())
    if previous not in (OLD_SHA256, NEW_SHA256):
        raise RuntimeError('Existing R38 installer differs from both reviewed versions')
    return {
        'local_head': local,
        'remote_head': remote,
        'source_guard': 'PASS',
        'installer_state': ('PATCHED' if previous == NEW_SHA256 else 'BASELINE'),
        'corrected_pin': CORRECT_R9_BLOB,
        'tracked_changes': tracked_changes,
    }


def preview_corrected_source_guard() -> dict[str, object]:
    """Verify the corrected R38 installer without changing on-disk code."""
    spec = importlib.util.spec_from_file_location('r38r1_in_memory_guard', REPLACEMENT)
    if spec is None or spec.loader is None:
        raise RuntimeError('Cannot load reviewed R38 installer replacement')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.PACKAGE = R38
    module.ROOT = ROOT
    return module.verify_checkout()


def repair(*, dry_run: bool) -> dict[str, object]:
    """DryRun is read-only; regular run replaces exactly one reviewed pin."""
    state = verify_checkout()
    preview = preview_corrected_source_guard()
    if preview['source_guard'] != 'PASS':
        raise RuntimeError('R38 source guard preview did not pass')
    if not dry_run and state['installer_state'] == 'BASELINE':
        raw = TARGET.read_bytes()
        sep = b'\r\n' if b'\r\n' in raw else b'\n'
        replacement = normalize(REPLACEMENT.read_bytes()).replace(b'\n',sep)
        TARGET.write_bytes(replacement)
        state = verify_checkout()
        if state['installer_state'] != 'PATCHED':
            raise RuntimeError('Corrected R38 installer failed post-install verification')
    state['r38_repaired_preview'] = True
    return state


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    result = repair(dry_run=args.dry_run)
    p = 'PHASE174_R3R7R38R1_'
    for key in ('local_head','remote_head','source_guard','installer_state',
                'corrected_pin','r38_repaired_preview'):
        print(p + key.upper() + '=' + str(result[key]))
    print(p + 'MODE=' + ('DRYRUN' if args.dry_run else 'INSTALLED'))
    print(p + 'GATE=PASS_R38R1_ONE_CHARACTER_SOURCE_PIN_REPAIRED')
    print('(END)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

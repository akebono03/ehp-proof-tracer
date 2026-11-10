"""R55R1: fix only str-vs-bytes comparison inside R55 Source Guard.

The original R55 renderer patch and inference pipeline remain unchanged.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / 'phase174_r3_r7_r55_common_exactness_intro' / 'source_guard.py'
R55_PATCH = ROOT / 'phase174_r3_r7_r55_common_exactness_intro' / 'patch.py'
REVIEWED_HEAD = '40db3a00ca8be58e589e0949e6a70dcedd3b9cf5'
BEFORE_SHA256 = '6b5edb3268c05d98fffdb2c8fcd067711d71aeaca53d67ab4b260a8ea16a02ac'
AFTER_SHA256 = 'f3f2734a99eeb2b151ada8924a461d3666dc2bc914526564498fa2dc37a562fa'
R55_PATCH_SHA256 = '2fb88d528e4f884780cf8428ae0e49754318032d029843aed91a67f6008b2c80'
BEFORE_EXPRESSION = 'installed=(norm(actual)==norm(desired))'
AFTER_EXPRESSION = 'installed=(norm(actual)==desired)'


def normalized_bytes(blob: bytes) -> bytes:
    """Treat Windows and Unix end-of-line conventions alike."""
    return blob.replace(b'\r\n', b'\n')


def digest(blob: bytes) -> str:
    """Hash exactly the normalized UTF-8 bytes of a reviewed file."""
    return hashlib.sha256(normalized_bytes(blob)).hexdigest()


def safe_git(*args: str) -> str:
    """Return a Git observation; never stage, reset, clean or commit."""
    process = subprocess.run(
        ('git',) + args, cwd=ROOT, capture_output=True,
        check=True, encoding='utf-8', errors='replace',
    )
    return process.stdout.strip()


def validate_repository() -> dict[str, object]:
    """Require the R54 merged HEAD and only R55's reviewed renderer edit."""
    if Path(safe_git('rev-parse', '--show-toplevel')).resolve() != ROOT.resolve():
        raise RuntimeError('R55R1 must be extracted immediately inside repository root')
    if safe_git('branch', '--show-current') != 'develop':
        raise RuntimeError('R55R1 requires develop')
    local_head = safe_git('rev-parse', 'HEAD')
    remote_line = safe_git('ls-remote', 'origin', 'refs/heads/develop').splitlines()
    remote_head = remote_line[0].split()[0] if remote_line else ''
    if local_head != REVIEWED_HEAD or remote_head != REVIEWED_HEAD:
        raise RuntimeError('R55R1 requires reviewed local/remote develop HEAD')
    if safe_git('diff', '--cached', '--name-only'):
        raise RuntimeError('R55R1 forbids staged file changes')
    modified = tuple(safe_git('diff', '--name-only').splitlines())
    if modified not in ((), ('phase168_r3_5_model_renderer.py',)):
        raise RuntimeError('Unreviewed tracked changes: ' + repr(modified))
    if not R55_PATCH.is_file() or digest(R55_PATCH.read_bytes()) != R55_PATCH_SHA256:
        raise RuntimeError('R55 original patch.py source differs from reviewed ZIP')
    if not TARGET.is_file():
        raise RuntimeError('R55 source_guard.py must already be extracted')
    source = TARGET.read_bytes()
    current = digest(source)
    if current not in (BEFORE_SHA256, AFTER_SHA256):
        raise RuntimeError('R55 source guard is neither reviewed before nor after source')
    return {
        'local_head': local_head,
        'remote_head': remote_head,
        'tracked_changes': modified,
        'source_guard_state': 'FIXED' if current == AFTER_SHA256 else 'ORIGINAL',
        'new_givens': 0,
        'new_mathematical_rules': 0,
        'production_files_changed': 0,
        'full_pytest': False,
    }


def corrected_source(source: bytes) -> bytes:
    """Apply the reviewed one-expression change, preserving line endings."""
    decoded = normalized_bytes(source).decode('utf-8-sig')
    if decoded.count(AFTER_EXPRESSION) == 1 and decoded.count(BEFORE_EXPRESSION) == 0:
        return source
    if decoded.count(BEFORE_EXPRESSION) != 1 or decoded.count(AFTER_EXPRESSION) != 0:
        raise RuntimeError('R55R1 reviewed expression occurs an unexpected number of times')
    result = source.replace(BEFORE_EXPRESSION.encode('utf-8'), AFTER_EXPRESSION.encode('utf-8'), 1)
    if digest(result) != AFTER_SHA256:
        raise RuntimeError('R55R1 result differs from reviewed complete source')
    return result


def apply_fix(*, dry_run: bool = False) -> dict[str, object]:
    """Apply only the R55 guard fix; support repeated dry/run invocations."""
    state = validate_repository()
    before = TARGET.read_bytes()
    after = corrected_source(before)
    if not dry_run and before != after:
        TARGET.write_bytes(after)
    if not dry_run:
        final = validate_repository()
        if final['source_guard_state'] != 'FIXED':
            raise RuntimeError('R55R1 fix failed postcondition')
    return {
        **state,
        'dry_run': dry_run,
        'source_guard_fixed': (not dry_run),
        'source_guard_already_fixed': before == after,
        'modified_files': 0 if dry_run or before == after else 1,
        'target': 'phase174_r3_r7_r55_common_exactness_intro/source_guard.py',
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    state = apply_fix(dry_run=args.dry_run)
    prefix = 'PHASE174_R3R7R55R1_'
    for key, value in state.items():
        print(prefix + key.upper() + '=' + str(value))
    print(prefix + 'GATE=' + (
        'PASS_R55R1_SOURCE_GUARD_DRYRUN' if args.dry_run else
        'PASS_R55R1_SOURCE_GUARD_FIXED'
    ))
    print('(END)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

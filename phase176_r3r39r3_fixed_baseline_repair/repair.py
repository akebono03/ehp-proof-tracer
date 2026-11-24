"""Repair only R3R39 line endings against its immutable pre-change Git blob."""
from __future__ import annotations

import argparse
import difflib
import subprocess
from pathlib import Path

from phase176_r3r39_public_equality_transport.apply import updated_source

ROOT = Path(__file__).resolve().parent.parent
TARGET = 'phase165_r52_r9_shared_math.py'
BASE = '8033d70c5ee67626b278918be15484c688ed146e'
BASE_BLOB = '359fc9e6be767d4b8b48549213a69244c4dbf7ce'


def expected_bytes(baseline: bytes) -> bytes:
    if b'\r' in baseline or baseline.startswith(b'\xef\xbb\xbf'):
        raise ValueError('UNEXPECTED_BASELINE_ENCODING')
    text = baseline.decode('utf-8')
    patched = updated_source(text)
    changes = list(difflib.ndiff(text.splitlines(keepends=True),
                                patched.splitlines(keepends=True)))
    if sum(s.startswith('+ ') for s in changes) != 9 or any(
            s.startswith('- ') for s in changes):
        raise ValueError('EXPECTED_EXACT_NINE_INSERTIONS')
    return patched.encode('utf-8')


def representation(raw: bytes, expected: bytes) -> str:
    if raw == expected:
        return 'LF'
    if raw == expected.replace(b'\n', b'\r\n'):
        return 'CRLF'
    raise ValueError('UNRELATED_OR_INCOMPLETE_SOURCE_REFUSED')


def git(root: Path, *args: str, data: bytes | None = None) -> bytes:
    return subprocess.check_output(['git', *args], cwd=root, input=data)


def inspect(root: Path, baseline: bytes, *, dry_run: bool) -> dict[str, str]:
    expected = expected_bytes(baseline)
    path = root / TARGET
    head = git(root, 'show', 'HEAD:' + TARGET)
    index = git(root, 'show', ':' + TARGET)
    current = path.read_bytes()
    states = {name: representation(raw, expected) for name, raw in (
        ('HEAD', head), ('INDEX', index), ('WORKTREE', current))}
    if head != index and index != expected:
        raise ValueError('UNEXPECTED_STAGED_REPRESENTATION')
    # Verify Git's actual clean conversion before any write. No object is stored.
    desired_hash = git(root, 'hash-object', '--stdin', '--no-filters', data=expected)
    filtered_hash = git(root, 'hash-object', '--stdin', '--path=' + TARGET, data=expected)
    if filtered_hash != desired_hash:
        raise ValueError('GIT_FILTER_WOULD_CHANGE_EXPECTED_LF_BLOB')
    if not dry_run and current != expected:
        path.write_bytes(expected)
    if not dry_run and path.read_bytes() != expected:
        raise ValueError('WORKTREE_WRITE_VERIFICATION_FAILED')
    states['WORKTREE_AFTER'] = representation(path.read_bytes(), expected)
    states['EXPECTED_BLOB'] = desired_hash.decode('ascii').strip()
    states['COMMIT_REQUIRED'] = str(head != expected)
    return states


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if git(ROOT, 'rev-parse', BASE + ':' + TARGET).decode('ascii').strip() != BASE_BLOB:
        raise ValueError('BASELINE_BLOB_MISMATCH')
    baseline = git(ROOT, 'show', BASE + ':' + TARGET)
    states = inspect(ROOT, baseline, dry_run=args.dry_run)
    for key, value in states.items():
        print('PHASE176_R3R39R3_' + key + '=' + value)
    print('PHASE176_R3R39R3_GATE=' + ('PASS_R3R39R3_DRYRUN' if args.dry_run else 'PASS_R3R39R3_FIXED_BASELINE_WORKTREE'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

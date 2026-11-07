"""Guarded, exact whole-file R18 audit correction; no production code edits."""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path('phase174_r3_r7_r18_delta_image_surjectivity/audit.py')
REPLACEMENT = Path(__file__).resolve().parent / 'replacement_audit.py.txt'
BEFORE_SHA256 = 'e0e0c986762f76dc601b0cdf6c01d81eece696dc2bb5f593ca0fd2debf045c73'
AFTER_SHA256 = '7ff6ab7b4f4b7595c6e16216e8c3a8e1edf3845cc4dcfdb3165879e4c7f57aaa'
REVIEWED_R17_HEAD = '4d59298949c14dc02d8bfb6ec28da4624ed980da'
REVIEWED_R18_HEAD = '7ecd12f28b5943b105ac6a953be69b44eae4a26e'
R18_PACKAGE_PREFIX = 'phase174_r3_r7_r18_delta_image_surjectivity/'
R18_AUDIT = TARGET.as_posix()
SOURCE_FILES = (
    'phase174_r3_r7_r18_delta_image_surjectivity/rule.py',
    'phase174_r3_r7_r18_delta_image_surjectivity/run.ps1',
    'phase174_r3_r7_r18_delta_image_surjectivity/tests/test_audit.py',
    'phase174_r3_r7_r18_delta_image_surjectivity/tests/test_rule.py',
)
BACKUP = (
    Path(os.environ.get('LOCALAPPDATA', tempfile.gettempdir()))
    / 'EHPProofTracerAudit' / 'phase174_r3_r7_r18r1'
    / 'audit_original.py'
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str, root: Path = ROOT) -> str:
    return subprocess.run(
        ('git',) + args, cwd=root, check=True, text=True,
        capture_output=True, encoding='utf-8', errors='replace',
    ).stdout.strip()


def git_bytes(*args: str, root: Path = ROOT) -> bytes:
    return subprocess.run(
        ('git',) + args, cwd=root, check=True, capture_output=True,
    ).stdout


def exact_replacement() -> bytes:
    data = REPLACEMENT.read_bytes()
    if digest(data) != AFTER_SHA256:
        raise RuntimeError('Unreviewed R18R1 replacement content')
    compile(data.decode('utf-8'), R18_AUDIT, 'exec')
    return data


def source_state(root: Path = ROOT) -> str:
    data = (root / TARGET).read_bytes()
    value = digest(data)
    if value == BEFORE_SHA256:
        return 'ORIGINAL'
    if value == AFTER_SHA256 and data == exact_replacement():
        return 'PATCHED'
    raise RuntimeError('R18 audit.py does not match either reviewed source state')


def verify_host(*, patched: bool, root: Path = ROOT) -> dict[str, str]:
    if Path(git('rev-parse', '--show-toplevel', root=root)).resolve() != root.resolve():
        raise RuntimeError('Extract R18R1 under the repo root')
    if git('branch', '--show-current', root=root) != 'develop':
        raise RuntimeError('Expected develop branch')
    local = git('rev-parse', 'HEAD', root=root)
    remote = git('ls-remote', 'origin', 'refs/heads/develop', root=root).split()[0]
    if remote != REVIEWED_R18_HEAD or local not in (REVIEWED_R17_HEAD, REVIEWED_R18_HEAD):
        raise RuntimeError('Unreviewed local/remote HEAD; refuse automatic patch')
    if git('diff', '--cached', '--name-only', root=root):
        raise RuntimeError('Staged changes need separate review')
    changed = tuple(git('diff', '--name-only', root=root).splitlines())
    permitted = (R18_AUDIT,) if patched and local == REVIEWED_R18_HEAD else ()
    if changed != permitted:
        raise RuntimeError('Unexpected tracked changes: ' + repr(changed))
    git_bytes('merge-base', '--is-ancestor', REVIEWED_R17_HEAD, REVIEWED_R18_HEAD, root=root)
    commits = git('rev-list', REVIEWED_R17_HEAD + '..' + REVIEWED_R18_HEAD, root=root).splitlines()
    paths = git('diff', '--name-only', REVIEWED_R17_HEAD, REVIEWED_R18_HEAD, root=root).splitlines()
    if len(commits) != 1 or not paths or any(not p.startswith(R18_PACKAGE_PREFIX) for p in paths):
        raise RuntimeError('Unreviewed R18 merge contents')
    source = git_bytes('show', 'origin/develop:' + R18_AUDIT, root=root)
    if digest(source) != BEFORE_SHA256:
        raise RuntimeError('Remote reviewed R18 audit.py changed')
    if source_state(root=root) != ('PATCHED' if patched else 'ORIGINAL'):
        raise RuntimeError('R18 audit.py in unexpected state')
    for path in SOURCE_FILES:
        local_source = root / path
        if not local_source.is_file():
            raise RuntimeError('Missing R18 reviewed source: ' + path)
        committed = git_bytes('show', 'origin/develop:' + path, root=root)
        if local_source.read_bytes() != committed:
            raise RuntimeError('R18 reviewed package source mismatch: ' + path)
    exact_replacement()
    return {'local': local, 'remote': remote, 'state': source_state(root=root)}


def apply(root: Path = ROOT) -> str:
    state = source_state(root=root)
    verify_host(patched=state == 'PATCHED', root=root)
    if state == 'PATCHED':
        if not BACKUP.is_file() or digest(BACKUP.read_bytes()) != BEFORE_SHA256:
            raise RuntimeError('Missing reviewed R18R1 backup for an already applied patch')
        return 'ALREADY_APPLIED'
    before = (root / TARGET).read_bytes()
    updated = exact_replacement()
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if BACKUP.exists() and BACKUP.read_bytes() != before:
        raise RuntimeError('Unexpected existing R18R1 backup')
    BACKUP.write_bytes(before)
    tmp = (root / TARGET).with_suffix('.r18r1.tmp')
    if tmp.exists():
        raise RuntimeError('Temporary patch file exists; inspect before retry')
    try:
        tmp.write_bytes(updated)
        os.replace(tmp, root / TARGET)
    finally:
        if tmp.exists():
            tmp.unlink()
    verify_host(patched=True, root=root)
    return 'APPLIED'


def rollback(root: Path = ROOT) -> str:
    if source_state(root=root) == 'ORIGINAL':
        return 'ALREADY_ORIGINAL'
    if not BACKUP.is_file():
        raise RuntimeError('Original R18 audit backup missing')
    original = BACKUP.read_bytes()
    if digest(original) != BEFORE_SHA256:
        raise RuntimeError('Stored backup does not match original source')
    (root / TARGET).write_bytes(original)
    return 'RESTORED'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--dry-run', action='store_true')
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--verify', action='store_true')
    mode.add_argument('--rollback', action='store_true')
    args = parser.parse_args()
    if args.rollback:
        outcome = rollback()
    elif args.apply:
        outcome = apply()
    else:
        state = source_state()
        verify_host(patched=state == 'PATCHED')
        if args.verify and state != 'PATCHED':
            raise RuntimeError('Expected applied R18R1 patch')
        outcome = 'PASS_PREFLIGHT_' + state if args.dry_run else 'PASS_VERIFIED_PATCH'
    print('PHASE174_R3R7R18R1_GUARD=' + outcome)
    print('PHASE174_R3R7R18R1_TARGET=' + R18_AUDIT)
    print('(END)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

"""Install one reviewed, minimal rule-function replacement with exact-source guards."""
from __future__ import annotations

import argparse
from hashlib import sha1, sha256
from pathlib import Path
import shutil
import subprocess
import os

TARGET = Path('phase173_r4_r1_source_bound_56/rule.py')
EXPECTED_BLOB = 'e05ada41cbcf53e8b755428afd245ba2da619fa8'
EXPECTED_PATCH_SHA256 = '1d63582af0e1632ac733e9dcb764a2afd6a1c3583f00acb88b56ce8b0d8964ce'
REVIEWED_SOURCES = {
    'phase165_r3_recursive_search.py': '06009bfcf57f99cac58c229d99c53f16324692d0',
    'phase165_r57_r20_general_specialization.py': 'e09603bee51d776cd4326a95930fc9c41f272a1b',
    'phase165_r52_r9_shared_math.py': '2718c55789af7f442ac2c086d016d3d6f7ca3133',
    'phase173_r4_r1_lemma54_source_bridge/source.py': 'a37bf7447194d72526522366944778c386c8966c',
    'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314',
}


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ('git', *args), cwd=root, capture_output=True,
        text=True, encoding='utf-8', check=True,
    ).stdout.strip()


def blob_hash(data: bytes) -> str:
    """Compute the Git blob identity for exactly the supplied raw content."""
    prefix = b'blob ' + str(len(data)).encode('ascii') + b'\x00'
    return sha1(prefix + data).hexdigest()


def normalize_line_endings(data: bytes) -> bytes:
    return data.replace(b'\r\n', b'\n')


def proposed_bytes(root: Path) -> bytes:
    source = root / 'phase173_r4_r1_diagonal_inference_fix' / 'replacement_rule.py'
    if not source.is_file():
        raise RuntimeError('Replacement rule payload is missing')
    content = normalize_line_endings(source.read_bytes())
    if 'SourceBoundGoal(diagonal, diagonal_source)' not in content.decode('utf8'):
        raise RuntimeError('Replacement lacks the reviewed scoped diagonal')
    if sha256(content).hexdigest() != EXPECTED_PATCH_SHA256:
        raise RuntimeError('Replacement file differs from the reviewed patch')
    return content


def preflight(root: Path) -> str:
    if git(root, 'branch', '--show-current') != 'develop':
        raise RuntimeError('Only the reviewed develop branch is supported')
    if git(root, 'rev-parse', 'HEAD:' + TARGET.as_posix()) != EXPECTED_BLOB:
        raise RuntimeError('The committed target rule has changed; no patch applied')
    if git(root, 'rev-parse', 'HEAD') != git(root, 'rev-parse', 'origin/develop'):
        raise RuntimeError('Local HEAD differs from origin/develop')
    for name, expected in REVIEWED_SOURCES.items():
        if git(root, 'rev-parse', 'HEAD:' + name) != expected:
            raise RuntimeError('Reviewed dependency blob changed: ' + name)
    target = root / TARGET
    if not target.is_file():
        raise RuntimeError('Reviewed target file is missing')
    original = normalize_line_endings(target.read_bytes())
    replacement = proposed_bytes(root)
    state = 'NEW' if blob_hash(original) == EXPECTED_BLOB else 'ALREADY_INSTALLED' if original == replacement else 'UNREVIEWED'
    if state == 'UNREVIEWED':
        raise RuntimeError('Unreviewed target worktree content; refusing overwrite')
    if git(root, 'diff', '--cached', '--name-only', '--', TARGET.as_posix()):
        raise RuntimeError('Staged changes to the target must not be overwritten')
    # Avoid making any change when an unreviewed patch is staged or present.
    return state


def install(root: Path) -> str:
    state = preflight(root)
    if state == 'ALREADY_INSTALLED':
        return state
    destination = root / TARGET
    before = destination.read_bytes()
    backup = Path(os.environ.get('LOCALAPPDATA', str(Path.home()))) / (
        'EHPProofTracerRecovery/phase173_r4_r1_diagonal_inference_fix/original_rule.py'
    )
    backup.parent.mkdir(parents=True, exist_ok=True)
    if backup.exists() and normalize_line_endings(backup.read_bytes()) != normalize_line_endings(before):
        raise RuntimeError('An unrelated backup exists; refusing overwrite')
    if not backup.exists():
        shutil.copy2(destination, backup)
    destination.write_bytes(proposed_bytes(root))
    return 'INSTALLED'


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    state = preflight(root)
    print('PHASE173_R4_R1_DIAGONAL_SOURCE_GUARD=PASS')
    print('PHASE173_R4_R1_DIAGONAL_PATCH_STATE=' + state)
    if args.dry_run:
        print('PHASE173_R4_R1_DIAGONAL_DRY_RUN=PASS')
        return 0
    outcome = install(root)
    print('PHASE173_R4_R1_DIAGONAL_INSTALL=' + outcome)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

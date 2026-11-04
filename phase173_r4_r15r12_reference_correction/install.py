"""Fail-closed installer for reviewed reference projection and Web math fixes."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess

from .patch import CHANGED_PATHS, changed_units, patch_source

EXPECTED_HEAD = 'e2996ec2ff496203f94daa9bc22550c5e69a6b11'
EXPECTED_BLOBS = {
    'phase168_r3_37c_reference_projection.py': '63c10c79a94df66e6b3f9ed9e2ad9d81f39f481e',
    'phase168_r3_3_proof_narrative_model.py': '2e8def26cfdd9444d480f149e0ae7a2c2d53b525',
    'web_group_proof_common.py': '2a7b6f47a6445f6b4c51d6eeeffa7645d2a48e1f',
    'phase169_r4g_hopf_reference/tests/test_r4g_hopf_reference.py': '7970809e62c3a334210498550df9b6ca296b68f4',
    'phase169_r4e_citation_binding/tests/test_r4e_citation_binding.py': '1ddb4a47322799f3b3eaaa5705da5316ad57007b',
}


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ('git', *args), cwd=root, check=True, capture_output=True,
        text=True, encoding='utf-8', errors='replace',
    )
    return completed.stdout.strip()


def preflight(root: Path) -> dict[str, tuple[bytes, bytes]]:
    root = root.resolve()
    if git(root, 'branch', '--show-current') != 'develop':
        raise RuntimeError('R15R12 requires branch develop')
    head = git(root, 'rev-parse', 'HEAD')
    remote = git(root, 'rev-parse', 'origin/develop')
    if head != EXPECTED_HEAD or remote != EXPECTED_HEAD:
        raise RuntimeError(
            f'Unreviewed HEAD: local={head}, remote={remote}; expected {EXPECTED_HEAD}'
        )
    if git(root, 'diff', '--cached', '--name-only'):
        raise RuntimeError('Staged source changes require review')
    updated: dict[str, tuple[bytes, bytes]] = {}
    for rel in CHANGED_PATHS:
        path = root / rel
        if not path.is_file():
            raise RuntimeError('Missing reviewed file: ' + rel)
        blob = git(root, 'hash-object', f'--path={rel}', rel)
        if blob != EXPECTED_BLOBS[rel]:
            raise RuntimeError(f'Unreviewed or already patched file: {rel}: {blob}')
        old = path.read_bytes()
        new = patch_source(rel, old)
        if old == new:
            raise RuntimeError('Patch did not change ' + rel)
        updated[rel] = (old, new)
    return updated


def full_units(root: Path, updates: dict[str, tuple[bytes, bytes]]) -> None:
    output = root / 'phase173_r4_r15r12_reference_correction' / 'FULL_CHANGED_UNITS.md'
    chunks = ['# R15R12 Complete changed units', '',
              'All modified functions and their complete module imports appear below.', '']
    for rel in CHANGED_PATHS:
        chunks.extend((changed_units(rel, updates[rel][0]), ''))
    output.write_text('\n'.join(chunks) + '\n', encoding='utf-8')
    print('PHASE173_R4_R15R12_FULL_CHANGED_UNITS=' + str(output), flush=True)


def install(root: Path) -> None:
    updates = preflight(root)
    directory = root / 'phase173_r4_r15r12_reference_correction'
    backups = directory / 'backups'
    state_path = directory / 'installed_state.json'
    if state_path.exists():
        raise RuntimeError('Prior R15R12 installation state already exists')
    backups.mkdir(parents=True, exist_ok=True)
    for rel, (original, _) in updates.items():
        target = backups / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(original)
    written = []
    try:
        for rel, (_, updated) in updates.items():
            target = root / rel
            temp = target.with_name(target.name + '.r15r12.tmp')
            try:
                temp.write_bytes(updated)
                os.replace(temp, target)
            finally:
                if temp.exists():
                    temp.unlink()
            written.append(rel)
        state_path.write_text(json.dumps({
            'expected_head': EXPECTED_HEAD,
            'changed_files': list(CHANGED_PATHS),
            'production_file_count': len(CHANGED_PATHS),
        }, indent=2) + '\n', encoding='utf-8')
    except Exception:
        for rel in reversed(written):
            (root / rel).write_bytes((backups / rel).read_bytes())
        raise
    full_units(root, updates)
    print('PHASE173_R4_R15R12R1_PATCHED_FILES=5', flush=True)


def restore(root: Path) -> None:
    directory = root / 'phase173_r4_r15r12_reference_correction'
    state_path = directory / 'installed_state.json'
    if not state_path.is_file():
        raise RuntimeError('No R15R12 installation to restore')
    state = json.loads(state_path.read_text(encoding='utf-8'))
    if state.get('expected_head') != EXPECTED_HEAD or tuple(state.get('changed_files', ())) != CHANGED_PATHS:
        raise RuntimeError('Invalid R15R12 state file')
    backups = directory / 'backups'
    for rel in CHANGED_PATHS:
        backup = backups / rel
        if not backup.is_file():
            raise RuntimeError('Missing backup: ' + rel)
        # Refuse to overwrite subsequent user edits: expected patch has to match.
        current = (root / rel).read_bytes()
        if current != patch_source(rel, backup.read_bytes()):
            raise RuntimeError('Production file changed after installation: ' + rel)
    for rel in CHANGED_PATHS:
        (root / rel).write_bytes((backups / rel).read_bytes())
    state_path.unlink()
    print('PHASE173_R4_R15R12_RESTORED=PASS', flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--dry-run', action='store_true')
    mode.add_argument('--install', action='store_true')
    mode.add_argument('--restore', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    if args.restore:
        restore(root)
    elif args.dry_run:
        updates = preflight(root)
        full_units(root, updates)
        print('PHASE173_R4_R15R12_SOURCE_GUARD=PASS', flush=True)
        print('PHASE173_R4_R15R12_DRY_RUN=PASS', flush=True)
        print('PHASE173_R4_R15R12_PRODUCTION_EDIT=NONE', flush=True)
    else:
        install(root)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

"""DryRun and hash-guarded installation of one whole-function renderer change.

No Git index mutations, staging, resetting, cleaning, or commits.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from .patch import HELPER, transform

ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
TARGET = 'phase168_r3_5_model_renderer.py'
TARGET_PATH = ROOT / TARGET
REVIEWED_REMOTE = 'a4e01bcafcd2afd295c61843bbaa597a6262f75a'
ALLOWED_LOCAL_HEADS = frozenset((
    'aa25a9930d36b61e7588d1ef8e5916a766b569e6',
    REVIEWED_REMOTE,
))
REVIEWED_BLOB = '53a542ee5903def81a87ecb11a35be31d7143341'
R2_STATE = ROOT / 'phase173_r4_r15r17r2_unsupported_given_clean' / 'installed_state.json'
R1_STATE = ROOT / 'phase173_r4_r15r17_unified_model' / 'installed_state.json'
BACKUP = PKG / 'renderer_before_r3r3.backup'
STATE = PKG / 'installed_state.json'
REVIEW = PKG / 'FULL_CHANGED_UNITS.md'


def git(*args: str) -> str:
    run = subprocess.run(
        ['git', '--no-pager', *args], cwd=ROOT, capture_output=True,
        text=True, encoding='utf-8', errors='replace',
    )
    if run.returncode:
        raise RuntimeError('Git command failed: ' + ' '.join(args) + ': ' + run.stderr.strip())
    return run.stdout.strip()


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def check_prerequisites() -> None:
    branch = git('branch', '--show-current')
    local = git('rev-parse', 'HEAD')
    remote = git('rev-parse', 'origin/develop')
    print(f'R15R17R3R3_LOCAL_HEAD={local}')
    print(f'R15R17R3R3_REMOTE_HEAD={remote}')
    if branch != 'develop' or local not in ALLOWED_LOCAL_HEADS or remote != REVIEWED_REMOTE:
        raise RuntimeError('Unreviewed Git branch or HEAD; no production writes')
    if git('rev-parse', f'HEAD:{TARGET}') != REVIEWED_BLOB:
        raise RuntimeError('Unreviewed renderer Git blob')
    for option in (('--name-only',), ('--cached', '--name-only')):
        if git('diff', *option, '--', TARGET):
            raise RuntimeError('Existing staged or unstaged renderer modifications')
    if not R1_STATE.is_file() or not R2_STATE.is_file():
        raise RuntimeError('R15R17-R1 and R2 installed_state.json must exist')
    r1 = json.loads(R1_STATE.read_text(encoding='utf-8'))
    r2 = json.loads(R2_STATE.read_text(encoding='utf-8'))
    if len(r1.get('files', {})) != 5:
        raise RuntimeError('R1 state is not complete')
    if r2.get('target') != TARGET or r2.get('installed_sha256') != digest(TARGET_PATH.read_bytes()):
        raise RuntimeError('Renderer is not the reviewed installed R2 state')


def reviewed_proposal() -> tuple[bytes, bytes]:
    check_prerequisites()
    original = TARGET_PATH.read_bytes()
    if b'\r\n' in original and b'\n' in original.replace(b'\r\n', b''):
        raise RuntimeError('Mixed line endings in renderer')
    normalized = original.replace(b'\r\n', b'\n').decode('utf-8')
    updated = transform(normalized)
    ast.parse(updated, filename=TARGET)
    changed = updated.encode('utf-8')
    if b'\r\n' in original:
        changed = changed.replace(b'\n', b'\r\n')
    if changed == original:
        raise RuntimeError('Renderer proposal has no changes')
    return original, changed


def complete_function(source: str, name: str) -> str:
    source = source.replace('\r\n', '\n')
    tree = ast.parse(source)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(functions) != 1:
        raise RuntimeError('Missing unique reviewed function: ' + name)
    node = functions[0]
    first = min((deco.lineno for deco in node.decorator_list), default=node.lineno)
    return '\n'.join(source.splitlines()[first-1:node.end_lineno])


def produce_review(changed: bytes) -> None:
    source = changed.decode('utf-8').replace('\r\n', '\n')
    lines = [
        '# Phase 173 R15R17-R3R3 Full Changed Units', '',
        '## Scope', '',
        f'- `{TARGET}` — new `project_typed_open_goal_displays()` before `render_model_backed_narrative_markdown()`',
        f'- `{TARGET}` — entire `render_model_backed_narrative_markdown()` function replaced',
        '- Production module imports and other functions/classes are unchanged.',
        '- Existing typed goals, cited steps and status are never mutated.', '',
        '## New function (complete)', '', '```python',
        complete_function(source, 'project_typed_open_goal_displays'), '```', '',
        '## Replacement function (complete)', '', '```python',
        complete_function(source, 'render_model_backed_narrative_markdown'), '```', '',
        '## New tests (complete, including imports)', '',
    ]
    for path in sorted((PKG / 'tests').glob('test_*.py')):
        lines.extend((f'### `{path.name}`', '', '```python',
                      path.read_text(encoding='utf-8'), '```', ''))
    REVIEW.write_text('\n'.join(lines), encoding='utf-8', newline='\n')
    print('R15R17R3R3_FULL_CHANGED_UNITS=' + str(REVIEW.relative_to(ROOT)))


def install(proposal: tuple[bytes, bytes], before: str) -> None:
    if STATE.exists() or BACKUP.exists():
        raise RuntimeError('Existing R3R3 state or backup, refusing overwrite')
    original, changed = proposal
    BACKUP.write_bytes(original)
    state = {
        'target': TARGET,
        'original_sha256': digest(original),
        'installed_sha256': digest(changed),
        'git_index_tree': before,
    }
    STATE.write_text(json.dumps(state, indent=2), encoding='utf-8')
    try:
        TARGET_PATH.write_bytes(changed)
        if digest(TARGET_PATH.read_bytes()) != state['installed_sha256']:
            raise RuntimeError('Installed renderer SHA256 mismatch')
        if git('write-tree') != before:
            raise RuntimeError('Git index was changed during install')
    except BaseException:
        TARGET_PATH.write_bytes(original)
        STATE.unlink(missing_ok=True)
        BACKUP.unlink(missing_ok=True)
        raise
    print('R15R17R3R3_INSTALL=PASS')
    print('R15R17R3R3_GIT_INDEX_PRESERVED=PASS')


def restore() -> None:
    if not BACKUP.is_file() or not STATE.is_file():
        raise RuntimeError('R3R3 installation state or backup missing')
    state = json.loads(STATE.read_text(encoding='utf-8'))
    original = BACKUP.read_bytes()
    if state.get('target') != TARGET or digest(original) != state.get('original_sha256'):
        raise RuntimeError('R3R3 backup integrity failed')
    if digest(TARGET_PATH.read_bytes()) != state.get('installed_sha256'):
        raise RuntimeError('Renderer modified after installation; refusing restore')
    before = git('write-tree')
    if before != state.get('git_index_tree'):
        raise RuntimeError('Git index changed since installation; refusing restore')
    TARGET_PATH.write_bytes(original)
    STATE.unlink()
    BACKUP.unlink()
    if git('write-tree') != before:
        raise RuntimeError('Git index changed during restore')
    print('R15R17R3R3_RESTORE=PASS')
    print('R15R17R3R3_GIT_INDEX_PRESERVED=PASS')


def main() -> int:
    args = argparse.ArgumentParser()
    args.add_argument('--dry-run', action='store_true')
    args.add_argument('--restore', action='store_true')
    parsed = args.parse_args()
    if parsed.restore:
        restore()
        return 0
    before = git('write-tree')
    proposal = reviewed_proposal()
    produce_review(proposal[1])
    if git('write-tree') != before:
        raise RuntimeError('Git index changed during preflight')
    if parsed.dry_run:
        print('R15R17R3R3_DRY_RUN=PASS')
        print('R15R17R3R3_PRODUCTION_WRITES=NONE')
        print('R15R17R3R3_GIT_INDEX_PRESERVED=PASS')
        return 0
    install(proposal, before)
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, TypeError, OSError, ValueError, SyntaxError) as exc:
        print('R15R17R3R3_ERROR=' + str(exc), file=sys.stderr)
        raise SystemExit(1)

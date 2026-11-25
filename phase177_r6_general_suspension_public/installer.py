"""Pinned minimal R6 shared provider connection; preserve actual worktree EOL."""
from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import subprocess
import tempfile

from phase177_r2_cited_511_reuse_audit.audit import git, matches_blob
from phase177_r5_general_suspension_equality_isolated.audit import PINS as R5_PINS

ROOT = Path(__file__).resolve().parents[1]
TARGET = 'phase165_r52_r9_shared_math.py'
HEAD = '166068e75b171bf66f08437f9329c2191c36e83a'
PINS = dict(R5_PINS, **{
    'phase177_r5_general_suspension_equality_isolated/rule.py': 'f8f94381103bf133393caf9c28ec18dfb8a7a006',
    'phase177_r5_general_suspension_equality_isolated/tests/test_rule.py': '803c6a8a6b203a286a19e1ec6a867a0bc11399dc',
    'phase169_r10b_registered_stable_family_binding/family_registry.py': '4e461795954cc3e7a34fe9e3b47f77d00e5faeda',
})
ANCHOR = '        return retain_ordered_root_expansions(proof_target, goal, merged)\n'
PATCH = (
    '        # Phase 177 R6: append general suspension equality proposals.\n'
    '        from phase177_r6_general_suspension_public.provider import (\n'
    '            expand_public_suspension_equality,\n'
    '        )\n'
    '        merged = merge_backward_expansions(merged, expand_public_suspension_equality(\n'
    '            goal, tuple(available) + prior_conclusions,\n'
    '        ))\n'
)


def normalize(raw: bytes) -> str:
    return raw.decode('utf-8-sig').replace('\r\n', '\n')


def proposed_source(source: str) -> str:
    if source.count(ANCHOR) != 1 or PATCH in source:
        raise ValueError('R6_ANCHOR_OR_DUPLICATE')
    tree = ast.parse(source)
    outer, = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'shared_expansion_provider']
    inner, = [n for n in ast.walk(outer) if isinstance(n, ast.FunctionDef) and n.name == 'expand']
    line = source[:source.index(ANCHOR)].count('\n') + 1
    if not inner.lineno < line <= inner.end_lineno:
        raise ValueError('R6_ANCHOR_OUTSIDE_SHARED_EXPAND')
    revised = source.replace(ANCHOR, PATCH + ANCHOR, 1)
    ast.parse(revised)
    return revised


def preflight() -> tuple[bytes, bytes, str]:
    if Path(git('rev-parse', '--show-toplevel')).resolve() != ROOT or git('branch', '--show-current') != 'develop':
        raise RuntimeError('WRONG_REPOSITORY_OR_BRANCH')
    local, remote = git('rev-parse', 'HEAD'), git('rev-parse', 'origin/develop')
    if (local, remote) != (HEAD, HEAD):
        raise RuntimeError(f'REVIEWED_HEAD_REQUIRED:expected={HEAD};local={local};origin/develop={remote}')
    if git('diff', '--cached', '--name-only'):
        raise RuntimeError('STAGED_CHANGES_REFUSED')
    if set(git('diff', '--name-only', 'HEAD').splitlines()) - {TARGET}:
        raise RuntimeError('UNRELATED_TRACKED_CHANGES_REFUSED')
    for name, pin in PINS.items():
        if git('rev-parse', 'HEAD:' + name) != pin:
            raise RuntimeError('HEAD_BLOB_CHANGED:' + name)
        if name != TARGET and not matches_blob((ROOT/name).read_bytes(), pin):
            raise RuntimeError('DEPENDENCY_CHANGED:' + name)
    baseline = subprocess.check_output(['git', 'show', 'HEAD:' + TARGET], cwd=ROOT)
    old = normalize(baseline)
    revised = proposed_source(old)
    current = (ROOT/TARGET).read_bytes()
    if normalize(current) not in (old, revised):
        raise RuntimeError('UNRELATED_TARGET_CHANGE_REFUSED')
    rest = current.replace(b'\r\n', b'')
    if b'\r' in rest or (b'\r\n' in current and b'\n' in rest):
        raise RuntimeError('UNSUPPORTED_MIXED_EOL')
    eol = '\r\n' if b'\r\n' in current else '\n'
    encoding = 'utf-8-sig' if current.startswith(b'\xef\xbb\xbf') else 'utf-8'
    return current, revised.replace('\n', eol).encode(encoding), revised


def full_review_source(source: str) -> str:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    imports = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    fn, = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'shared_expansion_provider']
    return ''.join(''.join(lines[n.lineno-1:n.end_lineno]) for n in imports) + '\n\n' + ''.join(lines[fn.lineno-1:fn.end_lineno])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    current, updated, revised = preflight()
    output = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/Path(__file__).parent.name
    output.mkdir(parents=True, exist_ok=True)
    review = output/'SHARED_FUNCTION_AND_IMPORTS_FULL.py.txt'
    review.write_text(full_review_source(revised), encoding='utf-8')
    (output/'SHARED_FILE_FULL.py.txt').write_text(revised, encoding='utf-8')
    if not args.dry_run and current != updated:
        (output/'shared_math.before').write_bytes(current)
        (ROOT/TARGET).write_bytes(updated)
    if not args.dry_run and (ROOT/TARGET).read_bytes() != updated:
        raise RuntimeError('INSTALL_BYTE_MISMATCH')
    print('PHASE177_R6_HEAD='+HEAD)
    print('PHASE177_R6_FULL_CODE='+str(review))
    print('PHASE177_R6_FULL_PYTEST=NOT_RUN')
    print('PHASE177_R6_GATE='+('PASS_R6_READ_ONLY_DRYRUN' if args.dry_run else 'PASS_R6_PUBLIC_HOOK_INSTALLED'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

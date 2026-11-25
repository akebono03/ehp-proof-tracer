"""Pinned R7R1 hook; no other production source is changed."""
from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import subprocess
import tempfile

from phase177_r2_cited_511_reuse_audit.audit import git, matches_blob
from phase177_r6_general_suspension_public.installer import full_review_source, normalize, PATCH as R6_PATCH
from phase177_r7_left_composition_reuse_audit.audit import PINS as R7_PINS

ROOT = Path(__file__).resolve().parents[1]
HEAD = '14a7fb8404da839c9ca13a818f3d6172db7f948a'
TARGET = 'phase165_r52_r9_shared_math.py'
PINS = dict(R7_PINS, **{
    'phase177_r6_general_suspension_public/installer.py': '19acff3bff6fdd084cf130d68e7d5af1b5476881',
    'phase177_r7_left_composition_reuse_audit/audit.py': 'd0951ce94a0deba8106ff641d2394c9389341b0e',
    'phase177_r7_left_composition_reuse_audit/tests/test_audit.py': '2296053d3458aea741440dab82cfcfc8199036ce',
})
ANCHOR = '        return retain_ordered_root_expansions(proof_target, goal, merged)\n'
PATCH = (
    '        # Phase 177 R7R1: existing typed left-composition congruence.\n'
    '        from phase177_r7r1_left_composition_public.provider import (\n'
    '            expand_public_left_composition,\n'
    '        )\n'
    '        merged = merge_backward_expansions(merged, expand_public_left_composition(goal))\n'
)


def proposed_source(source: str) -> str:
    if (source.count(ANCHOR) != 1 or source.count(R6_PATCH + ANCHOR) != 1
            or 'expand_public_left_composition' in source):
        raise ValueError('R7R1_ANCHOR_OR_DUPLICATE')
    tree = ast.parse(source)
    outer, = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'shared_expansion_provider']
    inner, = [n for n in ast.walk(outer) if isinstance(n, ast.FunctionDef) and n.name == 'expand']
    line = source[:source.index(ANCHOR)].count('\n') + 1
    if not inner.lineno < line <= inner.end_lineno:
        raise ValueError('R7R1_ANCHOR_OUTSIDE_SHARED_EXPAND')
    updated = source.replace(ANCHOR, PATCH + ANCHOR, 1)
    ast.parse(updated)
    return updated


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
    original = normalize(baseline)
    revised = proposed_source(original)
    current = (ROOT/TARGET).read_bytes()
    if normalize(current) not in (original, revised):
        raise RuntimeError('UNRELATED_TARGET_CHANGE_REFUSED')
    rest = current.replace(b'\r\n', b'')
    if b'\r' in rest or (b'\r\n' in current and b'\n' in rest):
        raise RuntimeError('UNSUPPORTED_MIXED_EOL')
    eol = '\r\n' if b'\r\n' in current else '\n'
    encoding = 'utf-8-sig' if current.startswith(b'\xef\xbb\xbf') else 'utf-8'
    return current, revised.replace('\n', eol).encode(encoding), revised


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
    print('PHASE177_R7R1_HEAD='+HEAD)
    print('PHASE177_R7R1_FULL_CODE='+str(review))
    print('PHASE177_R7R1_FULL_PYTEST=NOT_RUN')
    print('PHASE177_R7R1_GATE='+('PASS_R7R1_READ_ONLY_DRYRUN' if args.dry_run else 'PASS_R7R1_PUBLIC_HOOK_INSTALLED'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

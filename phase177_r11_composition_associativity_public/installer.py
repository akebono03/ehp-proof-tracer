"""Pinned R11 hook; no other production source is changed."""
from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import subprocess
import tempfile

from phase177_r2_cited_511_reuse_audit.audit import git, matches_blob
from phase177_r6_general_suspension_public.installer import full_review_source, normalize
from phase177_r8_unsigned_delta_public.installer import PATCH as R8_PATCH, ANCHOR
from phase177_r10_composition_associativity_isolated.audit import PINS as R10_PINS

ROOT = Path(__file__).resolve().parents[1]
HEAD = '527b4c1283edb178b63293a09bc96326ec1b0d71'
TARGET = 'phase165_r52_r9_shared_math.py'
PINS = dict(R10_PINS, **{
    'phase177_r10_composition_associativity_isolated/rule.py': '02d361bca9f273d1fe0a955d57a47e5705ab8abc',
    'phase177_r10_composition_associativity_isolated/tests/test_rule.py': '304799e8edfdc651387daa8a633d81442ca2d680',
    'phase177_r10_composition_associativity_isolated/audit.py': '77aef56591cd83fb41a10498b1eb94ccd191c210',
    'phase177_r9_delta_rhs_normalization_audit/audit.py': 'be32e413a49e71f0a15585712b09c3249c1ee06d',
    'phase177_r8_unsigned_delta_public/installer.py': '45408188a3b131235d087491bec24ecf70f3edb2',
    'phase177_r6_general_suspension_public/installer.py': '19acff3bff6fdd084cf130d68e7d5af1b5476881',
})
PATCH = (
    '        # Phase 177 R11: existing typed composition associativity equality.\n'
    '        from phase177_r10_composition_associativity_isolated.rule import (\n'
    '            expand_composition_associativity_equality,\n'
    '        )\n'
    '        merged = merge_backward_expansions(merged, expand_composition_associativity_equality(goal))\n'
)


def proposed_source(source: str) -> str:
    if (source.count(ANCHOR) != 1 or source.count(R8_PATCH + ANCHOR) != 1
            or 'expand_composition_associativity_equality' in source):
        raise ValueError('R11_ANCHOR_OR_DUPLICATE')
    tree = ast.parse(source)
    outer, = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'shared_expansion_provider']
    inner, = [n for n in ast.walk(outer) if isinstance(n, ast.FunctionDef) and n.name == 'expand']
    line = source[:source.index(ANCHOR)].count('\n') + 1
    if not inner.lineno < line <= inner.end_lineno:
        raise ValueError('R11_ANCHOR_OUTSIDE_SHARED_EXPAND')
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
    print('PHASE177_R11_HEAD='+HEAD)
    print('PHASE177_R11_FULL_CODE='+str(review))
    print('PHASE177_R11_FULL_PYTEST=NOT_RUN')
    print('PHASE177_R11_GATE='+('PASS_R11_READ_ONLY_DRYRUN' if args.dry_run else 'PASS_R11_PUBLIC_HOOK_INSTALLED'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

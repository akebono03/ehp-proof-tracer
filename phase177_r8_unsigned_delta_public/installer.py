"""Pinned R8 hook; no other production source is changed."""
from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import subprocess
import tempfile

from phase177_r2_cited_511_reuse_audit.audit import git, matches_blob
from phase177_r6_general_suspension_public.installer import full_review_source, normalize
from phase177_r7r1_left_composition_public.installer import PATCH as R7R1_PATCH
from phase177_r7_left_composition_reuse_audit.audit import PINS as R7_PINS

ROOT = Path(__file__).resolve().parents[1]
HEAD = '8f1edd43eee9ffcbba9cf6d6d0d3879a293ec967'
TARGET = 'phase165_r52_r9_shared_math.py'
PINS = dict(R7_PINS, **{
    'phase165_r52_r9_shared_math.py': 'fa94667652d789126fa6caa04de20516cf0a2f45',
    'phase177_r7r1_left_composition_public/provider.py': 'fe2205f2c44ffc81230a392b298eba6198f785df',
    'phase177_r7r1_left_composition_public/installer.py': 'ec95811a83aa7d4bc328497fd774ec2c89bd9cad',
    'phase177_r7r1_left_composition_public/tests/test_public.py': '5cfea456c9aa7f70d4325293df515549bd163451',
    'phase177_r3_unsigned_delta_composition_isolated/tests/test_rule.py': 'a30ef47bcea4e42c96209faff40c9005b532a124',
    'phase175_r4r10_cited_58_prop25_public/provider.py': 'be1d726fe98c0258685674ea41099aab1103f318',
    'phase175_r4r12r10r1_cited_511_public/provider.py': '6a57c443d8c69192ba58e213821cb62aac37553f',
    'phase175_r4r10_cited_58_prop25_public/source.py': 'b5162bdaac25e4578973816290207379734229f6',
    'phase177_r7_left_composition_reuse_audit/audit.py': 'd0951ce94a0deba8106ff641d2394c9389341b0e',
    'phase175_r4r12_public_two_summand_quotient/provider.py': '1b34fe0d2707a51af7acc52eaa7d38209e90dfa2',
    'phase175_r4r12r9_delta_generator_image_bridge/rule.py': 'cfff81f4662825b78f30f8b7b4886cb27333b6c2',
})
SETUP_ANCHOR = '    shared_provider_registry = build_shared_expansion_provider_registry(\n'
ANCHOR = '        return retain_ordered_root_expansions(proof_target, goal, merged)\n'
SETUP = (
    '    # Phase 177 R8: screened unsigned Prop 2.5 backward candidates.\n'
    '    from phase177_r8_unsigned_delta_public.provider import (\n'
    '        build_public_unsigned_delta_provider,\n'
    '    )\n'
    '    public_unsigned_delta = build_public_unsigned_delta_provider(bridge, prior_conclusions)\n'
)
PATCH = '        merged = merge_backward_expansions(merged, public_unsigned_delta(goal))\n'


def proposed_source(source: str) -> str:
    if (source.count(ANCHOR) != 1 or source.count(R7R1_PATCH + ANCHOR) != 1
            or source.count(SETUP_ANCHOR) != 1 or 'public_unsigned_delta' in source):
        raise ValueError('R8_ANCHOR_OR_DUPLICATE')
    tree = ast.parse(source)
    outer, = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'shared_expansion_provider']
    inner, = [n for n in ast.walk(outer) if isinstance(n, ast.FunctionDef) and n.name == 'expand']
    setup_line = source[:source.index(SETUP_ANCHOR)].count('\n') + 1
    line = source[:source.index(ANCHOR)].count('\n') + 1
    if not outer.lineno < setup_line < inner.lineno < line <= inner.end_lineno:
        raise ValueError('R8_ANCHOR_OUTSIDE_SHARED_EXPAND')
    updated = source.replace(SETUP_ANCHOR, SETUP + SETUP_ANCHOR, 1).replace(ANCHOR, PATCH + ANCHOR, 1)
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
    print('PHASE177_R8_HEAD='+HEAD)
    print('PHASE177_R8_FULL_CODE='+str(review))
    print('PHASE177_R8_FULL_PYTEST=NOT_RUN')
    print('PHASE177_R8_GATE='+('PASS_R8_READ_ONLY_DRYRUN' if args.dry_run else 'PASS_R8_PUBLIC_HOOK_INSTALLED'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

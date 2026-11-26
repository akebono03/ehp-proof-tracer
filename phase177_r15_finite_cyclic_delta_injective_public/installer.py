"""Install only the R15 public hook against a reviewed baseline."""
from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import subprocess
import tempfile

from phase177_r2_cited_511_reuse_audit.audit import git, matches_blob
from phase177_r6_general_suspension_public.installer import normalize, full_review_source
from phase177_r14_finite_cyclic_delta_injective_isolated.audit import PINS as R14_PINS

ROOT = Path(__file__).resolve().parents[1]
HEAD = 'da3e1b93d853fc9f4ded3b169af565561a1c7a95'
TARGET = 'phase165_r52_r9_shared_math.py'
PINS = dict(R14_PINS, **{
    'phase177_r14_finite_cyclic_delta_injective_isolated/audit.py': '95f8a5a942921af881aa094fa73497dccd8560b2',
    'web_group_proof.py': '2c66da9c8e80a13812a63b6adda34c9414d8413c',
    'phase165_r52_r3_web_adapter.py': 'dda215780c0468cf421592aff86c79b1f5482eed',
    'phase177_r14_finite_cyclic_delta_injective_isolated/rule.py': 'fba57005273dfdf795501df5f71b3822f4ecddfe',
    'phase177_r14_finite_cyclic_delta_injective_isolated/tests/test_rule.py': '385c4daaa7c43ac74082e20e314235144addd427',
    'phase176_r3r48_cited_finite_delta_kernel/rule.py': '86cc4a468ffd4601337bbef589a37fa46b449263',
    'phase165_r52_r2_search_adapter.py': 'c1d08b803a4d9f9e4e1ad5180a1487422f1cd191',
    'phase165_r55_nk_only_goal.py': 'e436879f578148fe5c30f5a34974bea3425108b2',
})
ANCHOR = '    # Phase 177 R8: screened unsigned Prop 2.5 backward candidates.\n'
PATCH = (
    '    # Phase 177 R15: expose existing finite cyclic Delta injectivity and summand order.\n'
    '    from phase177_r15_finite_cyclic_delta_injective_public.provider import build_public_finite_delta_injective_provider\n'
    '    extra_providers = tuple(extra_providers) + (\n'
    '        build_public_finite_delta_injective_provider(bridge=bridge, proof_target=proof_target),\n'
    '    )\n\n'
)


def proposed_source(source):
    if source.count(ANCHOR) != 1 or 'build_public_finite_delta_injective_provider' in source:
        raise ValueError('R15_ANCHOR_OR_DUPLICATE')
    tree = ast.parse(source)
    outer, = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'shared_expansion_provider']
    line = source[:source.index(ANCHOR)].count('\n') + 1
    if not outer.lineno < line <= outer.end_lineno:
        raise ValueError('R15_ANCHOR_OUTSIDE_SHARED_PROVIDER')
    revised = source.replace(ANCHOR, PATCH + ANCHOR, 1)
    ast.parse(revised)
    return revised


def preflight():
    if Path(git('rev-parse','--show-toplevel')).resolve() != ROOT or git('branch','--show-current') != 'develop':
        raise RuntimeError('WRONG_ROOT_OR_BRANCH')
    local, remote = git('rev-parse','HEAD'), git('rev-parse','origin/develop')
    if (local, remote) != (HEAD, HEAD):
        raise RuntimeError(f'REVIEWED_HEAD_REQUIRED:expected={HEAD};local={local};remote={remote}')
    if git('diff','--cached','--name-only'):
        raise RuntimeError('STAGED_CHANGES_REFUSED')
    if set(git('diff','--name-only','HEAD').splitlines()) - {TARGET}:
        raise RuntimeError('UNRELATED_TRACKED_CHANGES_REFUSED')
    for name, pin in PINS.items():
        if git('rev-parse','HEAD:'+name) != pin:
            raise RuntimeError('HEAD_BLOB_CHANGED:'+name)
        if name != TARGET and not matches_blob((ROOT/name).read_bytes(),pin):
            raise RuntimeError('DEPENDENCY_CHANGED:'+name)
    original = normalize(subprocess.check_output(['git','show','HEAD:'+TARGET],cwd=ROOT))
    revised = proposed_source(original)
    current = (ROOT/TARGET).read_bytes()
    if normalize(current) not in (original,revised):
        raise RuntimeError('UNRELATED_TARGET_CHANGE_REFUSED')
    rest = current.replace(b'\r\n',b'')
    if b'\r' in rest or (b'\r\n' in current and b'\n' in rest):
        raise RuntimeError('UNSUPPORTED_MIXED_EOL')
    eol = '\r\n' if b'\r\n' in current else '\n'
    encoding = 'utf-8-sig' if current.startswith(b'\xef\xbb\xbf') else 'utf-8'
    return current, revised.replace('\n',eol).encode(encoding), revised


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    current, updated, revised = preflight()
    output = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/Path(__file__).parent.name
    output.mkdir(parents=True,exist_ok=True)
    review = output/'SHARED_FUNCTION_AND_IMPORTS_FULL.py.txt'
    review.write_text(full_review_source(revised),encoding='utf-8')
    (output/'SHARED_FILE_FULL.py.txt').write_text(revised,encoding='utf-8')
    if not args.dry_run and current != updated:
        (output/'shared_math.before').write_bytes(current)
        (ROOT/TARGET).write_bytes(updated)
    if not args.dry_run and (ROOT/TARGET).read_bytes() != updated:
        raise RuntimeError('INSTALL_BYTE_MISMATCH')
    print('PHASE177_R15_HEAD='+HEAD)
    print('PHASE177_R15_FULL_CODE='+str(review))
    print('PHASE177_R15_GATE='+('PASS_R15_READ_ONLY_DRYRUN' if args.dry_run else 'PASS_R15_PUBLIC_HOOK_INSTALLED'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

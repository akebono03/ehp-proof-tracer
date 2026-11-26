"""Add one presentation hook; preserve the verified R17R1 display changes."""
from __future__ import annotations

import argparse
import ast
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile

from phase177_r2_cited_511_reuse_audit.audit import git, matches_blob
from phase177_r6_general_suspension_public.installer import normalize
from phase177_r17r1_finite_delta_reason_display.installer import (
    proposed_source as previous_typed_source,
    proposed_model_source as previous_model_source,
)

ROOT = Path(__file__).resolve().parents[1]
BASE = '6d61c70b985bef4550b35ce6fb3f6c130cd8631b'
TARGET = 'phase168_r3_27_typed_statement_projection.py'
MODEL = 'phase168_r3_5_model_renderer.py'
PREVIOUS = 'phase177_r17r1_finite_delta_reason_display'
PINS = {
    'phase175_r4r3_two_summand_quotient/rule.py': 'b854491dff8b42817c5e1fe2771e4f2dc2c16713',
    'phase175_r4r3_two_summand_quotient/tests/test_rule.py': '558651492f5af5ea330973dd2105f5f563d94281',
    'phase165_r12_r11_prop42_unified.py': '79752ec035244677ff6a54debff312e87a76fbf2',
    'phase165_r52_r9_shared_math.py': 'f4383a0c248fe62903203d1863df345740581c59',
    'toda_human_readable_renderer.py': 'cebe266300f31ce50abba8065235a6646915088d',
    'phase176_r3r55_equality_display_isolated/projection.py': 'f2bedfc04f96f27a771fbdebaa282fd9c2c9a075',
    'phase169_r10e5_composite_generator_image/rule.py': '01acace3eb273d47091421a61291ee54b51c369f',
    'phase177_r14_finite_cyclic_delta_injective_isolated/rule.py': 'fba57005273dfdf795501df5f71b3822f4ecddfe',
    'phase177_r15_finite_cyclic_delta_injective_public/tests/test_public.py': '8f6d2419933f3748a40749cbbdc3c65f4228fa24',
    'phase168_r3_27_typed_projection/tests/test_phase168_r3_27_typed_projection.py': 'e7e037f5ef9418a5de3a76e2a77c24cd39285a13',
}
BASE_PINS = {
    TARGET: '633fa68bd789ab3d4b61e34f47e952d35535b672',
    MODEL: 'c58c19f7234def48b743491c6a9c045345ac35e6',
}
PREVIOUS_SHA256 = {'installer.py': '0ded3e56803a63f08859bfc1435824a7a6df998ab3fc6a3c511d396e76e29e68', 'projection.py': '49d2ceff66ea3aeea9239245cc3afa7669af696e257c395b1e9d975422b9c1fa', 'tests/test_display.py': 'b99a97ce27b239e92880ae2b1194e469458722d1b99af9f5680bef8719168437'}
ANCHOR = '    if finite_delta_reason is not None:\n        return finite_delta_reason\n'
PATCH = (
    '    from phase177_r17r3_rank_two_quotient_display.projection import project_rank_two_quotient_reason\n'
    '    quotient_reason = project_rank_two_quotient_reason(statement, step)\n'
    '    if quotient_reason is not None:\n'
    '        return quotient_reason\n'
)


def proposed_source(source):
    if source.count(ANCHOR) != 1 or 'project_rank_two_quotient_reason' in source:
        raise ValueError('R17R3_ANCHOR_OR_DUPLICATE')
    tree = ast.parse(source)
    function, = [node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name == 'typed_sentence']
    line = source[:source.index(ANCHOR)].count('\n')+1
    if not function.lineno < line < function.end_lineno:
        raise ValueError('R17R3_ANCHOR_OUTSIDE_TYPED_SENTENCE')
    revised = source.replace(ANCHOR,ANCHOR+PATCH,1)
    ast.parse(revised)
    return revised


def git_source(ref, name):
    return subprocess.check_output(['git','show',ref+':'+name],cwd=ROOT)


def preflight():
    if Path(git('rev-parse','--show-toplevel')).resolve() != ROOT or git('branch','--show-current') != 'develop':
        raise RuntimeError('WRONG_ROOT_OR_BRANCH')
    head = git('rev-parse','HEAD')
    if head != git('rev-parse','origin/develop'):
        raise RuntimeError('LOCAL_REMOTE_HEAD_MISMATCH')
    git('merge-base','--is-ancestor',BASE,head)
    if git('diff','--cached','--name-only'):
        raise RuntimeError('STAGED_CHANGES_REFUSED')
    if set(git('diff','--name-only','HEAD').splitlines()) - {TARGET,MODEL}:
        raise RuntimeError('UNRELATED_TRACKED_CHANGES_REFUSED')
    for name,pin in PINS.items():
        if git('rev-parse','HEAD:'+name) != pin or not matches_blob((ROOT/name).read_bytes(),pin):
            raise RuntimeError('DEPENDENCY_CHANGED:'+name)
    for name,digest in PREVIOUS_SHA256.items():
        if hashlib.sha256((ROOT/PREVIOUS/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest() != digest:
            raise RuntimeError('PREVIOUS_PACKAGE_CHANGED:'+name)
    baselines = {}
    for name,pin in BASE_PINS.items():
        raw = git_source(BASE,name)
        if not matches_blob(raw,pin):
            raise RuntimeError('REVIEWED_BASE_CHANGED:'+name)
        baselines[name] = normalize(raw)
    previous = previous_typed_source(baselines[TARGET])
    previous_model = previous_model_source(baselines[MODEL])
    revised = proposed_source(previous)
    for name,allowed in ((TARGET,(baselines[TARGET],previous,revised)),(MODEL,(baselines[MODEL],previous_model))):
        if normalize(git_source(head,name)) not in allowed:
            raise RuntimeError('UNREVIEWED_COMMITTED_SOURCE:'+name)
    if normalize((ROOT/MODEL).read_bytes()) != previous_model:
        raise RuntimeError('R17R1_MODEL_HOOK_MISSING_OR_CHANGED')
    current = (ROOT/TARGET).read_bytes()
    if normalize(current) not in (previous,revised):
        raise RuntimeError('R17R1_TYPED_HOOK_MISSING_OR_CHANGED')
    rest = current.replace(b'\r\n',b'')
    if b'\r' in rest or (b'\r\n' in current and b'\n' in rest):
        raise RuntimeError('UNSUPPORTED_MIXED_EOL')
    eol = '\r\n' if b'\r\n' in current else '\n'
    encoding = 'utf-8-sig' if current.startswith(b'\xef\xbb\xbf') else 'utf-8'
    return head,current,revised.replace('\n',eol).encode(encoding),revised


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    head,current,updated,revised = preflight()
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/Path(__file__).parent.name
    folder.mkdir(parents=True,exist_ok=True)
    review = folder/'TYPED_PROJECTION_FULL.py.txt'
    review.write_text(revised,encoding='utf-8')
    if not args.dry_run and current != updated:
        (folder/'typed_projection.before').write_bytes(current)
        (ROOT/TARGET).write_bytes(updated)
    if not args.dry_run and (ROOT/TARGET).read_bytes() != updated:
        raise RuntimeError('INSTALL_BYTE_MISMATCH')
    print('PHASE177_R17R3_HEAD='+head)
    print('PHASE177_R17R3_FULL_CODE='+str(review))
    print('PHASE177_R17R3_GATE='+('PASS_R17R3_READ_ONLY_DRYRUN' if args.dry_run else 'PASS_R17R3_PUBLIC_HOOK_INSTALLED'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

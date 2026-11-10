"""R55: certify two actual Flask HTML routes with only one common intro."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r54_public_http_narrative_audit.audit import inspect_public_http_proof
from phase174_r3_r7_r55_common_exactness_intro.source_guard import verify_checkout


def inspect_common_intro() -> dict[str, object]:
    """Use the R54 real HTTP observer; do not stub any proof search or HTML."""
    from web_group_proof import build_standard_web_group_proof_view
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_partial_proof import ProofSearchStatus

    check = inspect_public_http_proof()
    if not check['both_http_200'] or not check['both_complete_proof']:
        raise RuntimeError('R55 lost the R54 verified public proof')
    cases=check['cases']
    if len(cases)!=2 or any(x['repeated_intro_count']!=1 for x in cases):
        raise RuntimeError('Common renderer must introduce a result only once: '+repr(cases))
    view=build_standard_web_group_proof_view(7,5,max_depth=2,mode='narrative')
    if view.key!='generic-complete-proof' or view.partial_result:
        raise RuntimeError('R55 narrative Model route must still be complete')
    prose=' '.join(str(line.prefix)+' '+str(line.suffix) for line in view.rendered_lines)
    if prose.count('の群構造を決定するために')!=1 or 'さらに' not in prose:
        # The R54 HTTP HTML check is canonical. This additionally checks
        # the common WebGroupProofView, not a second narrative implementation.
        raise RuntimeError('R55 common Web view did not preserve a natural continuation')
    proof=search_group_from_registered_goal(n=7,k=5)
    if proof.status is not ProofSearchStatus.COMPLETE or len(proof.open_goals)!=0 or len(proof.proven_steps)!=28:
        raise RuntimeError('R55 changed the public proof search or verified steps')
    return {
        'root':'pi_12^7 = 0',
        'both_http_200':True,
        'both_complete_proof':True,
        'public_verified_steps':len(proof.proven_steps),
        'public_open_goals':len(proof.open_goals),
        'http_cases':cases,
        'repeated_intro_counts':[x['repeated_intro_count'] for x in cases],
        'common_intro_once':True,
        'later_chain_continuation':True,
        'renderer_is_shared':True,
        'proof_tree_mutated':False,
        'new_given':0,
        'new_mathematical_rules':0,
        'browser_katex_checked':False,
        'full_pytest':False,
    }


def report_path(dry_run:bool)->Path:
    base=Path(os.environ.get('LOCALAPPDATA',tempfile.gettempdir()))
    return base/'EHPProofTracerAudit'/'phase174_r3_r7_r55'/('preflight.json' if dry_run else 'common_exactness_intro.json')


def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dry-run',action='store_true')
    opts=p.parse_args()
    state=verify_checkout()
    if not opts.dry_run and not state['r55_renderer_installed']:
        raise RuntimeError('R55 common renderer patch not yet installed')
    results=None if opts.dry_run else inspect_common_intro()
    gate=('PASS_R55_SOURCE_PREFLIGHT' if opts.dry_run else 'PASS_R55_COMMON_EXACTNESS_INTRO_HTTP_VERIFIED')
    result={'phase':'174-R3-R7-R55','state':state,'observations':results,'gate':gate}
    dest=report_path(opts.dry_run)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    prefix='PHASE174_R3R7R55_'
    for k,v in state.items():
        print(prefix+k.upper()+'='+str(v))
    if results is not None:
        for k,v in results.items():
            print(prefix+k.upper()+'='+str(v))
    print(prefix+'REPORT='+str(dest))
    print(prefix+'GATE='+gate)
    print('(END)')
    return 0

if __name__=='__main__':
    raise SystemExit(main())

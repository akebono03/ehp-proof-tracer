"""Install and audit only the public R4 connection; no new proof rule."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

from phase178_r5_delta_surjective_public.installer import (
    ROOT, TARGET, full_review_source, git_text, preflight, require,
)

PREFIX = 'PHASE178_R5_'
TESTS = (
    'phase178_r4_delta_surjective_zero_suspension_isolated/tests/test_rule.py',
    'phase178_r5_delta_surjective_public/tests/test_installer.py',
)


def emit(key, value):
    print(PREFIX + key + '=' + str(value), flush=True)


def inspect_public_context():
    import phase165_r55_nk_only_goal as entry
    import phase165_r52_r2_search_adapter as adapter
    from unittest.mock import patch
    from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
    from phase178_r4_delta_surjective_zero_suspension_isolated.rule import RULE_NAME, delta_surjective_inputs
    from phase178_r1_k6_source_first_audit.audit import statement
    from phase165_r3_recursive_search import GoalExpansion
    from proof import ProofRule

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(9,3))
    goal = MapSurjective(TodaDeltaMap(TodaPrimaryGroup(9,5),TodaPrimaryGroup(7,2)))
    invocations = []
    real = adapter.search_registered_partial_proof

    def observed(*args, **kwargs):
        require((kwargs.get('n'), kwargs.get('k')) == (3,6), 'UNEXPECTED_SEARCH_COORDINATES')
        invocations.append(dict(kwargs))
        return real(*args, **kwargs)

    with patch.object(adapter, 'search_registered_partial_proof', observed):
        result = entry.search_group_from_registered_goal(n=3,k=6)
    require(len(invocations) == 1 and result.target == root.group, 'PUBLIC_CONTEXT_CAPTURE_FAILED')
    invocation = invocations[0]
    require(invocation['goal'] == root, 'ROOT_CHANGED')
    provider = invocation['expansion_provider']
    bridge = invocation['bridge']
    require(not any(link.step is not None and link.step.rule is ProofRule.GIVEN and link.step.conclusion == root for link in bridge.proof_links), 'ROOT_GIVEN_PRESENT')
    probes = []
    for n,q in ((2,7),(3,6),(4,9),(5,11),(8,18)):
        probe = MapSurjective(TodaDeltaMap(TodaPrimaryGroup(q+2,2*n+1),TodaPrimaryGroup(q,n)))
        required = delta_surjective_inputs(probe)
        options = tuple(provider(probe))
        matching = tuple(x for x in options if x.rule.name == RULE_NAME)
        require(len(matching)==1 and matching[0].subgoals==required, 'R4_PUBLIC_PROPOSAL_MISSING_OR_CHANGED:'+repr(probe))
        require(isinstance(matching[0],GoalExpansion), 'INVALID_PROPOSAL_TYPE')
        probes.append({'goal':statement(probe),'rule':RULE_NAME,'subgoals':[statement(x) for x in required]})
    for bad in (MapInjective(goal.map), MapSurjective(TodaDeltaMap(TodaPrimaryGroup(9,6),TodaPrimaryGroup(7,2))), MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(7,2),TodaPrimaryGroup(8,3)))):
        require(not any(x.rule.name==RULE_NAME for x in provider(bad)), 'R4_INVALID_GOAL_PROPOSED')
    exact, zero = delta_surjective_inputs(goal)
    child_reports = []
    for child in (exact,zero):
        options = tuple(provider(child))
        require(bool(options),'R4_CHILD_HAS_NO_PROPOSAL:'+repr(child))
        child_reports.append({'goal':statement(child),'rules':[x.rule.name for x in options]})
    delta_steps = [s for s in result.proven_steps if s.conclusion == goal]
    # The root currently stops at Delta injectivity. Do not substitute a proof
    # or change the root just to claim that this new route is accepted.
    emit('ROOT_STATUS',result.status.value)
    emit('ROOT_OPEN_GOALS',len(result.open_goals))
    emit('DELTA_SURJECTIVITY', 'ACCEPTED_IN_ROOT_SEARCH' if delta_steps else 'PUBLIC_CANDIDATE_ONLY')
    for row in child_reports:
        emit('CHILD',json.dumps(row,ensure_ascii=False))
    return {'root_status':result.status.value,'root_open_goals':[statement(x) for x in result.open_goals], 'root_step_count':len(result.proven_steps), 'delta_accepted_in_root_search':bool(delta_steps),'public_probes':probes,'children':child_reports,'new_given':0,'single_root_search':True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    folder_base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/Path(__file__).parent.name
    folder_base.mkdir(parents=True,exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_',dir=folder_base))
    report = {'gate':'FAIL_R5','dry_run':args.dry_run,'full_pytest':'NOT_RUN','new_rules':0,'new_given':0}
    try:
        head,current,updated,revised = preflight()
        emit('HEAD',head)
        report['head']=head
        review = folder/'SHARED_FUNCTION_AND_IMPORTS_FULL.py.txt'
        review.write_text(full_review_source(revised),encoding='utf-8')
        (folder/'SHARED_FILE_FULL.py.txt').write_text(revised,encoding='utf-8')
        emit('FULL_CODE',review)
        if args.dry_run:
            report['gate']='PASS_R5_READ_ONLY_DRYRUN'
        else:
            if current != updated:
                (folder/'shared_math.before').write_bytes(current)
                (ROOT/TARGET).write_bytes(updated)
            require((ROOT/TARGET).read_bytes()==updated,'INSTALL_BYTE_MISMATCH')
            report['audit']=inspect_public_context()
            command=[sys.executable,'-B','-m','pytest','-q','-p','no:cacheprovider','--import-mode=importlib',*TESTS]
            report['focused_command']=command
            subprocess.run(command,cwd=ROOT,check=True)
            check_head,check_current,check_updated,_=preflight()
            require(check_head==head and check_current==check_updated==updated,'POST_INSTALL_INTEGRITY_FAILED')
            require(git_text('diff','--name-only','HEAD')==TARGET,'EXPECTED_SINGLE_TRACKED_CHANGE')
            report['gate']='PASS_R5_DELTA_SURJECTIVITY_PUBLIC_CONNECTION'
    except Exception as exc:
        report.update(error=repr(exc),traceback=traceback.format_exc())
        emit('ERROR',repr(exc))
    (folder/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    emit('REPORT',folder/'report.json')
    emit('FULL_PYTEST','NOT_RUN')
    emit('GATE',report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__=='__main__':
    raise SystemExit(main())

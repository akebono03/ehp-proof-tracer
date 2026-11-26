"""Install and audit only the public R6 connection; no new proof rule."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

from phase178_r7_finite_group_cardinality_public.installer import (
    ROOT, TARGET, full_review_source, git_text, preflight, require,
)

PREFIX = 'PHASE178_R7_'
TESTS = (
    'phase178_r6_finite_group_cardinality_isolated/tests/test_rule.py',
    'phase178_r7_finite_group_cardinality_public/tests/test_installer.py',
    'phase178_r7_finite_group_cardinality_public/tests/test_provider.py',
)


def emit(key, value):
    print(PREFIX + key + '=' + str(value), flush=True)


def inspect_public_context():
    import phase165_r55_nk_only_goal as entry
    import phase165_r52_r2_search_adapter as adapter
    from unittest.mock import patch
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase169_r10e4_ordered_db_prior.db_prior import admitted_prior_group_step, verified_db_step
    from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
    from phase178_r6_finite_group_cardinality_isolated.rule import RULE_NAME
    from phase178_r1_k6_source_first_audit.audit import statement
    from proof import ProofRule, apply_inference_match, find_inference_matches_for_rule

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(9,3))
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
    for label, group in (('delta_domain',TodaPrimaryGroup(9,5)),
                         ('delta_codomain',TodaPrimaryGroup(7,2))):
        goal = FiniteGroupCardinality(group,2)
        prior = admitted_prior_group_step(group,proof_target=root,bridge=bridge)
        require(prior is not None and verified_db_step(prior,proof_target=root,bridge=bridge),'PRIOR_NOT_VERIFIED:'+label)
        options = tuple(x for x in provider(goal) if x.rule.name == RULE_NAME)
        matching = tuple(x for x in options if x.subgoals == (prior.conclusion,))
        require(len(matching)==1,'R6_PUBLIC_PRIOR_PROPOSAL_MISSING_OR_DUPLICATE:'+label)
        option = matching[0]
        matches = find_inference_matches_for_rule(option.rule,(prior,))
        require(len(matches)==1,'R6_REPLAY_MATCH_FAILED:'+label)
        replay = apply_inference_match(matches[0])
        require(replay.rule is ProofRule.INFERENCE and replay.conclusion == goal and replay.premises == (prior,), 'R6_REPLAY_FAILED:'+label)
        require(not any(x.rule.name==RULE_NAME for x in provider(FiniteGroupCardinality(group,3))), 'WRONG_CARDINALITY_PROPOSED:'+label)
        row = {'name':label,'goal':statement(goal),'premise':statement(prior.conclusion),
               'candidate_count':len(options),'verified_prior_replay':True,
               'accepted_in_root_search':any(s.conclusion==goal for s in result.proven_steps)}
        probes.append(row)
        emit('PROBE',json.dumps(row,ensure_ascii=False))
    emit('ROOT_STATUS',result.status.value)
    emit('ROOT_OPEN_GOALS',len(result.open_goals))
    emit('CARDINALITY','PUBLIC_CANDIDATES_AND_VERIFIED_PRIOR_REPLAY')
    return {'root_status':result.status.value,'root_open_goals':[statement(x) for x in result.open_goals],
            'root_step_count':len(result.proven_steps),'probes':probes,'new_given':0,'single_root_search':True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    folder_base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/Path(__file__).parent.name
    folder_base.mkdir(parents=True,exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_',dir=folder_base))
    report = {'gate':'FAIL_R7','dry_run':args.dry_run,'full_pytest':'NOT_RUN','new_rules':0,'new_given':0}
    try:
        head,current,updated,revised = preflight()
        emit('HEAD',head)
        report['head']=head
        review = folder/'SHARED_FUNCTION_AND_IMPORTS_FULL.py.txt'
        review.write_text(full_review_source(revised),encoding='utf-8')
        (folder/'SHARED_FILE_FULL.py.txt').write_text(revised,encoding='utf-8')
        emit('FULL_CODE',review)
        if args.dry_run:
            report['gate']='PASS_R7_READ_ONLY_DRYRUN'
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
            report['gate']='PASS_R7_FINITE_GROUP_CARDINALITY_PUBLIC_CONNECTION'
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

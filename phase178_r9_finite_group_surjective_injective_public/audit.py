"""Install and audit only the public R8 connection; no new proof rule."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

from phase178_r9_finite_group_surjective_injective_public.installer import (
    ROOT, TARGET, full_review_source, git_text, preflight, require,
)

PREFIX = 'PHASE178_R9_'
TESTS = (
    'phase178_r8_finite_group_surjective_injective_isolated/tests/test_rule.py',
    'phase178_r6_finite_group_cardinality_isolated/tests/test_rule.py',
    'phase178_r7_finite_group_cardinality_public/tests/test_provider.py',
    'phase178_r9_finite_group_surjective_injective_public/tests/test_installer.py',
    'phase178_r9_finite_group_surjective_injective_public/tests/test_provider.py',
)


def emit(key, value):
    print(PREFIX + key + '=' + str(value), flush=True)


def inspect_public_context(folder):
    from phase178_r1_k6_source_first_audit.audit import observe, statement
    from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
    from phase178_r8_finite_group_surjective_injective_isolated.rule import RULE_NAME, finite_surjective_injective_inputs
    from phase178_r4_delta_surjective_zero_suspension_isolated.rule import RULE_NAME as SURJ_RULE

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(9,3))
    mapping = TodaDeltaMap(TodaPrimaryGroup(9,5),TodaPrimaryGroup(7,2))
    goal = MapInjective(mapping)
    expected = [statement(g) for g in finite_surjective_injective_inputs(goal,2)]
    summary = observe(3,6,folder)
    detail = json.loads((folder/'n3_k6.json').read_text(encoding='utf-8'))
    emit('ROOT_STATUS',summary['status'])
    emit('ROOT_OPEN_GOALS',summary['open_goal_count'])
    emit('ROOT_STEPS',summary['proven_step_count'])
    emit('WEB_KEY',summary['web_key'])
    emit('TRUST_STATUS',summary['trust_status'])
    for row in detail['frontier']:
        emit('FRONTIER',json.dumps({'goal':row['goal'],'state':row['state'],
                                   'rules':[o['rule'] for batch in row['observed_expansions'] for o in batch['options']]},ensure_ascii=False))
    proposals = [o for batch in detail['provider_calls'] if batch['goal']==statement(goal)
                 for o in batch['options'] if o['rule']==RULE_NAME]
    require(bool(proposals) and all(o['subgoals']==expected for o in proposals), 'R8_PUBLIC_PROPOSAL_NOT_OBSERVED_OR_CHANGED')
    nodes = detail['tree']['nodes']
    root_nodes = [node for node in nodes if node['conclusion']==statement(root)]
    ancestors = set()
    def visit(index):
        if index in ancestors:
            return
        ancestors.add(index)
        for parent in nodes[index]['premises']:
            visit(parent)
    for node in root_nodes:
        visit(node['id'])
    accepted = [node for node in nodes if node['conclusion']==statement(goal) and node['inference_rule']==RULE_NAME]
    for node in accepted:
        require(node['rule']=='INFERENCE' and [nodes[i]['conclusion'] for i in node['premises']]==expected,'R8_ACCEPTED_PREMISES_CHANGED')
        require(all(nodes[i]['rule']=='INFERENCE' for i in node['premises']),'R8_UNPROVED_PARENT')
        require(nodes[node['premises'][2]]['inference_rule']==SURJ_RULE,'R4_SURJECTIVITY_ROUTE_NOT_USED')
    emit('DELTA_INJECTIVITY','ACCEPTED' if accepted else 'PUBLIC_CANDIDATE_ONLY')
    emit('TARGET_GIVEN_COUNT',summary['target_given_count'])
    require(summary['target_given_count']==0,'TARGET_GIVEN_PRESENT')
    require(not detail['screened_source_inventory']['target_group_given_links'],'TARGET_SOURCE_GIVEN_PRESENT')
    require(summary['web_error'] is None,'WEB_ERROR:'+str(summary['web_error']))
    complete = summary['status']=='complete'
    if complete:
        require(summary['complete_invariants_hold'] and detail['conclusion']==statement(root),'COMPLETE_PROOF_INVALID')
        require(len(root_nodes)==1 and root_nodes[0]['rule']=='INFERENCE','ROOT_NOT_INFERRED')
        require(any(node['id'] in ancestors for node in accepted),'R8_NOT_IN_ROOT_ANCESTRY')
    else:
        require(summary['status'] in ('partial','search_failed') and detail['conclusion'] is None and detail['open_goals'],'INCONSISTENT_PARTIAL_RESULT')
        require(summary['web_key']=='generic-partial-proof','PARTIAL_WEB_KEY_CHANGED')
    return dict(summary, r8_accepted=bool(accepted),r8_in_root_ancestry=any(node['id'] in ancestors for node in accepted),
                candidate_count=len(proposals),root_complete=complete, new_given=0,single_root_search=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    folder_base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/Path(__file__).parent.name
    folder_base.mkdir(parents=True,exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_',dir=folder_base))
    report = {'gate':'FAIL_R9','dry_run':args.dry_run,'full_pytest':'NOT_RUN','new_rules':0,'new_given':0}
    try:
        head,current,updated,revised = preflight()
        emit('HEAD',head)
        report['head']=head
        review = folder/'SHARED_FUNCTION_AND_IMPORTS_FULL.py.txt'
        review.write_text(full_review_source(revised),encoding='utf-8')
        (folder/'SHARED_FILE_FULL.py.txt').write_text(revised,encoding='utf-8')
        emit('FULL_CODE',review)
        if args.dry_run:
            report['gate']='PASS_R9_READ_ONLY_DRYRUN'
        else:
            if current != updated:
                (folder/'shared_math.before').write_bytes(current)
                (ROOT/TARGET).write_bytes(updated)
            require((ROOT/TARGET).read_bytes()==updated,'INSTALL_BYTE_MISMATCH')
            report['audit']=inspect_public_context(folder)
            command=[sys.executable,'-B','-m','pytest','-q','-p','no:cacheprovider','--import-mode=importlib',*TESTS]
            report['focused_command']=command
            subprocess.run(command,cwd=ROOT,check=True)
            check_head,check_current,check_updated,_=preflight()
            require(check_head==head and check_current==check_updated==updated,'POST_INSTALL_INTEGRITY_FAILED')
            require(git_text('diff','--name-only','HEAD')==TARGET,'EXPECTED_SINGLE_TRACKED_CHANGE')
            report['gate']=('PASS_R9_PUBLIC_CONNECTION_ROOT_COMPLETE' if report['audit']['root_complete'] else 'PASS_R9_PUBLIC_CONNECTION_FRONTIER_OPEN')
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

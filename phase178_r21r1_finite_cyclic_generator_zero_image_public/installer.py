"""Connect the verified R21 provider without changing its rule or source registry."""
import argparse
import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
HEAD = '73a77aedcebabb8b4c6a2ee2edf4df7e9ac8a3aa'
TARGET = 'phase165_r52_r9_shared_math.py'
R21 = 'phase178_r21_finite_cyclic_generator_zero_image_isolated/'
OLD_TEST = R21 + 'tests/test_rule.py'
R4C = 'phase169_r4c_pi64_suspension_iso/tests/test_r4c_pi64_suspension_iso.py'
PINS = {
    TARGET: '726da9783e96b5ecd82e2ca49b786fb488d8a1a7',
    OLD_TEST: 'e2994df8fbfffeb17c0493060ee0b2c89dd417ef',
    R21 + 'rule.py': '3ff46d65aee3c7ae2fdc3b3ba3f8c68d282d0b8d',
    R21 + 'audit.py': 'fee73d23982447d782af5e0f6b34d082276c3a95',
    'phase178_r20r1_suspension_isomorphism_bridge_public/installer.py': 'b6d7f1731dff5610df45c0af56e800c899f2973f',
    'phase178_r20r1_suspension_isomorphism_bridge_public/tests/test_public.py': 'dc3d88490e564708016c5c5ff0e69ba711cd2d23',
    'phase178_r1_k6_source_first_audit/audit.py': '4990d6ab37de46860a375d4d7a17207ed2daeb05',
    'phase178_r20f1_historical_guard_audit/audit.py': '41b23cb648ce3141d5ef7b43580a9d76f9c92bbc',
    'phase165_r57_r11_proof_order_gate.py': '1ad9dfe8bb3da061cbee0dbd7a11c196f3f50604',
    R4C: '165bd5dee76978dd5d3f0cca40b4890f14b9257b',
}
TESTS = (
    PACKAGE + '/tests/test_public.py', OLD_TEST,
    'phase174_r3_r7_r6_cyclic_generator_zero_image/tests/test_rule.py',
    'phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py',
    'phase178_r16_toda513_isolated/tests/test_registration.py',
    'phase178_r19_finite_cyclic_suspension_transport_isolated/tests/test_provider.py',
    'phase178_r20_suspension_isomorphism_bridge_isolated/tests/test_rule.py',
    'phase178_r20r1_suspension_isomorphism_bridge_public/tests/test_public.py',
)
ANCHOR = '        return retain_ordered_root_expansions(proof_target, goal, merged)\n'
INSERT = '''        # Phase 178 R21R1: append the verified cyclic generator zero-image provider.
        from phase178_r21_finite_cyclic_generator_zero_image_isolated.rule import (
            build_finite_cyclic_delta_zero_provider, valid_delta_zero_goal,
        )
        if valid_delta_zero_goal(goal):
            from phase169_r10e4_ordered_db_prior.db_prior import group_coordinates
            if group_coordinates(proof_target) is not None:
                delta_zero_provider = build_finite_cyclic_delta_zero_provider(
                    bridge=bridge, proof_target=proof_target,
                )
                for option in delta_zero_provider(goal):
                    if not any(old.rule.name == option.rule.name and old.subgoals == option.subgoals
                               for old in merged):
                        merged += (option,)
'''
TEST_EDITS = (
    ('    assert all(o.rule.name != r21.RULE_NAME for o in shared_expansion_provider(bridge,proof_target=root)(goal))\n',
     '    public = shared_expansion_provider(bridge,proof_target=root)(goal)\n'
     '    assert sum(o.rule.name == r21.RULE_NAME and o.subgoals == option.subgoals for o in public) == 1\n'),
    ("    print('R21_N6_DELTA_ZERO_ISOLATED_REPLAY=VERIFIED')",
     "    print('R21_N6_DELTA_ZERO_ISOLATED_REPLAY=VERIFIED')\n"
     "    print('R21R1_N6_PUBLIC_PROVIDER_MATCH=VERIFIED')"),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print('PHASE178_R21R1_' + key + '=' + str(value), flush=True)


def replace_once(text, old, new):
    require(text.count(old) == 1, 'MISSING_OR_AMBIGUOUS_ANCHOR:' + old)
    return text.replace(old, new, 1)


def proposed_source(text):
    require(INSERT not in text, 'ALREADY_CONNECTED_SOURCE')
    updated = replace_once(text, ANCHOR, INSERT + ANCHOR)
    ast.parse(updated)
    return updated


def proposed_test(text):
    for old, new in TEST_EDITS:
        text = replace_once(text, old, new)
    ast.parse(text)
    return text


def preflight(r1, previous):
    gt = r1.git_text
    require(Path(os.fsdecode(r1.git('rev-parse','--show-toplevel').strip())).resolve() == ROOT, 'WRONG_ROOT')
    require(gt('branch','--show-current') == 'develop', 'DEVELOP_REQUIRED')
    require(gt('rev-parse','HEAD') == gt('rev-parse','origin/develop') == HEAD, 'REVIEWED_HEAD_REQUIRED:' + HEAD)
    require(not gt('diff','--cached','--name-only'), 'STAGED_CHANGES_PRESENT')
    require(not os.environ.get('PYTEST_ADDOPTS','').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    writers = {TARGET: proposed_source, OLD_TEST: proposed_test}
    require(set(gt('diff','--name-only','HEAD').splitlines()) <= set(writers), 'UNRELATED_TRACKED_CHANGES')
    changes = {}
    for path, pin in PINS.items():
        require(gt('rev-parse','HEAD:'+path) == pin, 'PIN_CHANGED:' + path)
        file = ROOT/path
        if path not in writers:
            require(r1.blob_matches(file,pin), 'WORKTREE_PIN_CHANGED:' + path)
            continue
        base = previous.normalized(r1.git('show',HEAD+':'+path))
        updated = writers[path](base)
        raw = file.read_bytes()
        require(previous.normalized(raw) in (base,updated), 'UNREVIEWED_WORKTREE:' + path)
        changes[path] = (raw,previous.encode_like(updated,raw),updated)
    for path in TESTS:
        require((ROOT/path).is_file(), 'FOCUSED_TEST_MISSING:' + path)
    r1.git('diff','--check')
    return changes


def audit_public(r1, folder, report):
    from phase178_r21_finite_cyclic_generator_zero_image_isolated.rule import RULE_NAME
    from phase178_r16_toda513_isolated.source import canonical_513
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from toda_rules import TodaDeltaZeroStatement
    image = canonical_513()[1]
    goal = TodaDeltaZeroStatement(image.map)
    domain = exact_prior_database_result(11,2)
    report['groups'] = []
    for n in (2,3,4,5,6):
        summary = r1.worker(n,6,folder,180)
        report['groups'].append(summary)
        require('detail' in summary,'WORKER_FAILED:' + repr(summary))
        require(summary['web_error'] is None and summary['complete_invariants_hold']
                and summary['target_given_count'] == 0,'PUBLIC_TRUST_FAILURE:' + repr(summary))
        detail = json.loads(Path(summary['detail']).read_text(encoding='utf-8'))
        emit('GROUP',json.dumps({k: summary[k] for k in ('n','k','status','proven_step_count','open_goal_count','trust_status','target_given_count','web_key')},ensure_ascii=False))
        if n < 6:
            require(summary['status']=='complete' and summary['trust_status']=='VERIFIED'
                    and summary['open_goal_count']==0 and summary['web_key']=='generic-complete-proof',
                    'COMPLETED_GROUP_REGRESSION:' + str(n))
            continue
        require(summary['status'] in ('complete','partial'), 'N6_SEARCH_FAILED')
        require(detail['screened_source_inventory'] is not None and not detail['screened_source_inventory']['target_group_given_links'], 'SCREENED_TARGET_GIVEN')
        expected = [r1.statement(domain),r1.statement(image)]
        calls = [c for c in detail['provider_calls'] if c['goal']==r1.statement(goal)]
        require(any(o['rule']==RULE_NAME and o['subgoals']==expected for c in calls for o in c['options']), 'R21_CANDIDATE_NOT_IN_ACTUAL_SEARCH')
        nodes = {node['id']:node for node in detail['tree']['nodes']}
        matching = [node for node in nodes.values() if node['conclusion']==r1.statement(goal)
                    and node['inference_rule']==RULE_NAME and node['rule']=='INFERENCE']
        for node in matching:
            parents = [nodes[i] for i in node['premises']]
            require([p['conclusion'] for p in parents]==expected and all(p['rule']=='GIVEN' and not p['premises'] for p in parents), 'R21_PREMISES_CHANGED')
            require('DB prior: sphere.csv' in str(parents[0]['literature_reference']) and '(5.13)' in str(parents[1]['literature_reference']), 'R21_PROVENANCE_CHANGED')
        report['n6_delta_nodes'] = matching
        report['n6_delta_calls'] = calls
        report['n6_frontier'] = detail['frontier']
        emit('N6_DELTA_ZERO_CANDIDATE','REACHED')
        emit('N6_DELTA_ZERO_IN_TREE','VERIFIED' if matching and summary['status']=='complete' else 'OBSERVED_PARTIAL' if matching else 'NOT_IN_RETURNED_TREE')
        emit('N6_ROOT_STATUS',summary['status'])
        emit('N6_OPEN_GOALS',summary['open_goal_count'])
        if summary['status']=='complete':
            require(bool(matching),'COMPLETE_WITHOUT_EXPECTED_R21_ROUTE')
        for item in detail['frontier']:
            emit('FRONTIER',json.dumps(item,ensure_ascii=False))
        for line in detail['web']['rendered_lines']:
            print(line)
    emit('COMPLETED_K6_REGRESSION','4/4_VERIFIED')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    from phase178_r1_k6_source_first_audit import audit as r1
    from phase178_r20r1_suspension_isomorphism_bridge_public import installer as previous
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    base.mkdir(parents=True,exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_',dir=base))
    report = {'gate':'FAIL_R21R1','dry_run':args.dry_run,'new_math_rules':0,'new_given':0,'full_pytest':'NOT_RUN'}
    written = []
    try:
        changes = preflight(r1,previous)
        emit('HEAD',HEAD)
        previous.export_code(folder,changes)
        emit('FULL_CODE',folder)
        if args.dry_run:
            report['gate']='PASS_R21R1_DRYRUN'
        else:
            for path,(raw,updated,text) in changes.items():
                require((ROOT/path).read_bytes()==raw,'WORKTREE_CHANGED:' + path)
            for path,(raw,updated,text) in changes.items():
                if raw != updated:
                    written.append((path,raw,updated))
                    (ROOT/path).write_bytes(updated)
            before = r1.snapshot()
            command = [sys.executable,'-B','-m','pytest','-q','-s','--import-mode=importlib','-p','no:cacheprovider',*TESTS]
            report['focused_command']=command
            subprocess.run(command,cwd=ROOT,check=True)
            from phase178_r20f1_historical_guard_audit import audit as historical
            code, xml_path = historical.pytest_run((R4C,),folder,'historical_after_r21r1')
            report['historical_guard']=historical.classify_baseline(code,xml_path)
            emit('HISTORICAL_GUARD',report['historical_guard'])
            audit_public(r1,folder,report)
            require(r1.snapshot()==before,'REPOSITORY_CHANGED_DURING_AUDIT')
            after = preflight(r1,previous)
            require(all(raw==updated for raw,updated,text in after.values()),'POST_INSTALL_INTEGRITY_FAILED')
            report['gate']='PASS_R21R1_FINITE_CYCLIC_DELTA_ZERO_PUBLIC' + ('_WITH_HISTORICAL_GUARD_OPEN' if report['historical_guard']=='KNOWN_GUARD_REPRODUCED_OPEN' else '')
    except Exception as exc:
        for path,raw,updated in reversed(written):
            if (ROOT/path).read_bytes()==updated:
                (ROOT/path).write_bytes(raw)
        report.update(error=repr(exc),traceback=traceback.format_exc())
        emit('ERROR',repr(exc))
    (folder/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
    emit('REPORT',folder/'report.json')
    emit('NEW_TYPED_RULES',0)
    emit('NEW_MATH_RULES',0)
    emit('NEW_GIVEN',0)
    emit('FULL_PYTEST','NOT_RUN')
    emit('GATE',report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__=='__main__':
    raise SystemExit(main())

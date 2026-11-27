"""Read-only audit of the actual public n=7,k=6 proof and screened candidates."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
HEAD = '1d8c87dfc3aa3aac79aa86b5e2ae142541b02da0'
PINS = {
    'phase165_r52_r9_shared_math.py': '79c3fc2d14080c188ef9284119a6eccb832daac9',
    'phase178_r1_k6_source_first_audit/audit.py': '4990d6ab37de46860a375d4d7a17207ed2daeb05',
    'phase178_r18_n6_source_first_audit/audit.py': 'd9577c8d77c73e21e112a37f56942ecc7adbfdfe',
    'phase178_r19_finite_cyclic_suspension_transport_isolated/provider.py': 'c20a6c2d8466cd30adee8bb92ed61283c6c6fe9d',
    'phase178_r20_suspension_isomorphism_bridge_isolated/rule.py': '8d23ba92147c3fd151bd2648725a7fd8241ce4ac',
    'phase178_r21_finite_cyclic_generator_zero_image_isolated/rule.py': '3ff46d65aee3c7ae2fdc3b3ba3f8c68d282d0b8d',
    'phase178_r15_toda512_isolated/source.py': 'c0dedf1aa758adf6f7f925ea86ec7a85c5f994dc',
    'phase178_r15_toda512_isolated/provider.py': 'b7114fb01a851d0ad9a5a16ee794e4ec603b7d50',
    'phase178_r15_toda512_isolated/source_contract.py': 'b712da395b5e399009c131ae3d3ea6044fcf69e2',
    'phase178_r16_toda513_isolated/source.py': '73300491e27c4d4298e07d8b0bd9c6653328b609',
    'phase178_r16_toda513_isolated/source_contract.py': '8e6aa8beac6bc3c5f490f64b262aaa83d33a829b',
    'phase169_r10e4_ordered_db_prior/db_prior.py': '2ff19f92e10608f210fdb5fd3718f9ef9c71d91d',
    'phase168_r3_5_model_renderer.py': 'f622c3d134c2613a286dc126ba970641f9856a68',
    'phase178_r17r3_common_renderer/projection.py': '5a821266655fcf8a0684ee438060730a00b61a77',
    'phase177_r17r6r1_suspension_composition_display/projection.py': '95101b10162ce62fbe56ffcd8a25963ede107849',
    'phase178_r19_finite_cyclic_suspension_transport_isolated/tests/test_provider.py': '910766ecc613bda7470fcbf804783aea88678d93',
    'phase178_r20_suspension_isomorphism_bridge_isolated/tests/test_rule.py': 'fb6f340cfec0e9a7f31fa816cb13ca763c5cb277',
    'phase178_r21_finite_cyclic_generator_zero_image_isolated/tests/test_rule.py': '6e9a0f7548460a2a4fd6d24c2a6415f10fa18bfc',
    'phase178_r16_toda513_isolated/tests/test_registration.py': 'b16cbb51c8f7463237b7e31458cb8205041a993e',
    'phase178_r23_common_renderer_elision/tests/test_display.py': '31deb821841f3224774112aea1e38879d3bf85f5',
    'phase168_r3_41p13_trust_boundary/verification.py': '547464846ce574d227092a4aacb895d2e2dfefca',
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
    'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314',
}
SELF_FILES = frozenset(PACKAGE + '/' + name for name in (
    '__init__.py', 'audit.py', 'run.ps1', 'tests/test_audit.py',
))
TESTS = (
    PACKAGE + '/tests/test_audit.py',
    'phase178_r16_toda513_isolated/tests/test_registration.py',
    'phase178_r19_finite_cyclic_suspension_transport_isolated/tests/test_provider.py',
    'phase178_r20_suspension_isomorphism_bridge_isolated/tests/test_rule.py',
    'phase178_r21_finite_cyclic_generator_zero_image_isolated/tests/test_rule.py',
    'phase178_r23_common_renderer_elision/tests/test_display.py',
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print('PHASE178_R24_' + key + '=' + str(value), flush=True)


def store(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + '\n', encoding='utf-8')


def validate_scope(committed, dirty):
    require(set(committed) <= SELF_FILES, 'UNREVIEWED_COMMITTED_PATHS:' + repr(sorted(set(committed) - SELF_FILES)))
    require(not dirty, 'TRACKED_WORKTREE_NOT_CLEAN:' + repr(sorted(dirty)))


def preflight(r1):
    gt = r1.git_text
    require(Path(os.fsdecode(r1.git('rev-parse', '--show-toplevel').strip())).resolve() == ROOT, 'WRONG_ROOT')
    require(gt('branch', '--show-current') == 'develop', 'DEVELOP_REQUIRED')
    head = gt('rev-parse', 'HEAD')
    require(head == gt('rev-parse', 'origin/develop'), 'LOCAL_REMOTE_HEAD_MISMATCH')
    require(gt('merge-base', HEAD, head) == HEAD, 'REVIEWED_BASE_REQUIRED:' + HEAD)
    validate_scope(gt('diff', '--name-only', HEAD, head).splitlines(),
                   gt('diff', '--name-only', 'HEAD').splitlines())
    require(not gt('diff', '--cached', '--name-only'), 'STAGED_CHANGES_PRESENT')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    for path, pin in PINS.items():
        require(gt('rev-parse', head + ':' + path) == pin and r1.blob_matches(ROOT / path, pin), 'PIN_CHANGED:' + path)
    for path in TESTS:
        require((ROOT / path).is_file(), 'TEST_MISSING:' + path)
    check = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    require(check.returncode == 0, 'GIT_DIFF_CHECK:' + check.stdout + check.stderr)
    from phase178_r15_toda512_isolated.source_contract import verify_clause as verify_512
    from phase178_r16_toda513_isolated.source_contract import verify_clause as verify_513
    chapter = (ROOT / 'sources/toda/Toda_05_2.tex').read_text(encoding='utf-8-sig')
    return {'head': head, 'eq512_line': verify_512(chapter), 'eq513_line': verify_513(chapter)}


def summarize(summary, detail):
    """Do not promote an incomplete public result or a proposed rule to a proof."""
    require((summary['n'], summary['k']) == (7, 6), 'WRONG_TARGET')
    require(summary['status'] in ('complete', 'partial', 'search_failed', 'not_searched'), 'UNMEASURED_TARGET')
    require(summary['web_error'] is None and summary['web_key'] is not None, 'WEB_GAP')
    require(summary['target_given_count'] == 0 and summary['complete_invariants_hold'], 'TRUST_CONTRACT_FAILED')
    require(len(detail['open_goals']) == summary['open_goal_count'], 'OPEN_GOAL_COUNT_CHANGED')
    inventory = detail['screened_source_inventory']
    require(inventory is not None and not inventory['target_group_given_links'], 'SCREENED_ROOT_GIVEN_OR_MISSING_CONTEXT')
    complete = summary['status'] == 'complete'
    if complete:
        require(summary['trust_status'] == 'VERIFIED' and summary['open_goal_count'] == 0
                and summary['web_key'] == 'generic-complete-proof', 'COMPLETE_NOT_VERIFIED')
    frontier = [{'goal': item['goal'], 'state': item['state'],
                 'rules': list(dict.fromkeys(o['rule'] for batch in item['observed_expansions'] for o in batch['options']))}
                for item in detail['frontier']]
    return {'root_complete': complete, 'frontier': frontier,
            'provider_call_count': len(detail['provider_calls']), 'search_context': detail['search_context'],
            'screened_source_inventory': inventory}


def ancestry(nodes, start):
    seen, active = set(), set()

    def visit(i):
        require(i in nodes and i not in active, 'INVALID_PROOF_GRAPH')
        if i in seen:
            return
        active.add(i)
        for parent in nodes[i]['premises']:
            visit(parent)
        active.remove(i)
        seen.add(i)
    visit(start)
    return seen


def probe_active_context(invocation, summary, detail):
    """Inspect the exact active bridge after search; no candidate is applied."""
    from expression import Zero
    from homotopy_groups import (FiniteCyclicGroup, TodaPrimaryGroup, TodaDeltaMap,
        TodaSuspensionMap, TodaSuspensionIsomorphismStatement, TodaEHPExactnessWindow)
    from phase165_r14_r6_generic_iso import GeneratorImage, MapInjective, MapSurjective, MapIsomorphism
    from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
    from toda_rules import TodaDeltaZeroStatement, TodaProp42ExactnessStatement
    from phase178_r15_toda512_isolated.source import canonical_512
    from phase178_r16_toda513_isolated.source import canonical_513
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result, admitted_prior_group_step, verified_db_step
    from phase176_r3r48_cited_finite_delta_kernel.rule import linked_cited_steps
    from phase178_r19_finite_cyclic_suspension_transport_isolated.provider import suspension_transport_inputs
    from phase178_r21_finite_cyclic_generator_zero_image_isolated.rule import finite_cyclic_delta_zero_inputs, RULE_NAME as ZERO_RULE
    from phase178_r20_suspension_isomorphism_bridge_isolated.rule import RULE_NAME as ISO_RULE
    from phase169_r10e5_composite_generator_image.rule import component_image_obligations
    from phase178_r1_k6_source_first_audit import audit as r1
    from proof import Relation

    root, bridge, provider = (invocation[k] for k in ('goal', 'bridge', 'expansion_provider'))
    require(root == exact_prior_database_result(7,6) and type(root) is Relation
            and root.lhs == TodaPrimaryGroup(13,7) and type(root.rhs) is FiniteCyclicGroup
            and root.rhs.order == 2, 'ROOT_PRESENTATION_CHANGED')
    lower = exact_prior_database_result(6,6)
    image = canonical_513()[2]
    domain = exact_prior_database_result(13,1)
    upper = canonical_512(6)
    require(type(lower) is Relation and lower.lhs == TodaPrimaryGroup(12,6)
            and type(lower.rhs) is FiniteCyclicGroup and lower.rhs.order == 2, 'PREVIOUS_STEM_ROW_CHANGED')
    require(type(domain) is Relation and domain.lhs == TodaPrimaryGroup(14,13)
            and type(domain.rhs) is FiniteCyclicGroup and domain.rhs.order == 2, 'DELTA_DOMAIN_ROW_CHANGED')
    a, b, c = lower.lhs, root.lhs, domain.lhs
    h, d = TodaPrimaryGroup(13,13), TodaPrimaryGroup(11,6)
    e = TodaSuspensionMap(a,b)
    delta = TodaDeltaZeroStatement(TodaDeltaMap(c,a))
    require(image.map == delta.map and image.target_generator == Zero()
            and upper.statement == MapInjective(TodaDeltaMap(h,d)), 'SOURCE_MAP_CHANGED')
    transport = suspension_transport_inputs(root, lower)
    require(transport is not None, 'TRANSPORT_INPUTS_MISSING')
    _, typed_iso, composite = transport
    generic, inj, surj = MapIsomorphism(e), MapInjective(e), MapSurjective(e)
    factors = component_image_obligations(composite)
    require(factors is not None, 'COMPOSITE_INPUTS_MISSING')
    de = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(source_term=c,middle_term=a,target_term=b,first_map=EHP_DELTA_MAP,second_map=EHP_E_MAP))
    eh = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(source_term=a,middle_term=b,target_term=h,first_map=EHP_E_MAP,second_map=EHP_H_MAP))
    hd = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(source_term=b,middle_term=h,target_term=d,first_map=EHP_H_MAP,second_map=EHP_DELTA_MAP))
    targets = (
        ('ROOT',root), ('PRIOR_STEM_GROUP',lower), ('TYPED_ISO',typed_iso),
        ('GENERIC_ISO',generic), ('E_INJECTIVE',inj), ('DELTA_ZERO',delta),
        ('DELTA_DOMAIN_GROUP',domain), ('CITED_513_IMAGE',image), ('DELTA_E_EXACT',de),
        ('E_SURJECTIVE',surj), ('UPPER_DELTA_INJECTIVE',upper.statement), ('CITED_512',upper),
        ('H_DELTA_EXACT',hd), ('E_H_EXACT',eh), ('COMPOSITE_IMAGE',composite),
        ('FACTOR_1',factors[0]), ('FACTOR_2',factors[1]),
    )
    nodes = {node['id']:node for node in detail['tree']['nodes']}
    root_scope = set()
    if summary['status'] == 'complete':
        require(detail['conclusion'] == r1.statement(root), 'WRONG_ROOT_CONCLUSION')
        roots = [i for i in detail['tree']['observed_steps'] if nodes[i]['conclusion'] == r1.statement(root)]
        require(len(roots) == 1 and nodes[roots[0]]['rule'] == 'INFERENCE', 'ROOT_INFERENCE_MISSING')
        root_scope = ancestry(nodes, roots[0])
    def prior_info(statement):
        step = admitted_prior_group_step(statement.lhs, proof_target=root, bridge=bridge)
        return {'eligible': step is not None and step.conclusion == statement
                and verified_db_step(step, proof_target=root, bridge=bridge),
                'presentation': r1.statement(statement)}
    sources = {'512_screened_link_count': len(linked_cited_steps(bridge,upper)),
               '513_screened_link_count': len(linked_cited_steps(bridge,image)),
               '513_generator_matches_db': image.source_generator == domain.rhs.generator,
               'previous_stem_order_matches_root': lower.rhs.order == root.rhs.order,
               'prior_checks': {'DELTA_DOMAIN':prior_info(domain), 'PREVIOUS_STEM':prior_info(lower)}}
    rows = []
    for name, goal in targets:
        g = r1.statement(goal)
        observed = [batch for batch in detail['provider_calls'] if batch['goal'] == g]
        options = provider(goal)
        rows.append({'name':name, 'goal':g, 'actual_provider_visits':len(observed),
                     'actual_tree_node_ids':[i for i,node in nodes.items() if node['conclusion']==g],
                     'root_ancestor_ids':[i for i in sorted(root_scope) if nodes[i]['conclusion']==g],
                     'linked_fixed_given_count':len(linked_cited_steps(bridge,goal)),
                     'candidate_count':len(options),
                     'candidates':[{'rule':opt.rule.name,'subgoals':[r1.statement(s) for s in opt.subgoals]} for opt in options]})
    def has(name, rule, required):
        if required is None:
            return False
        row = next(r for r in rows if r['name']==name)
        return any(o['rule']==rule and o['subgoals']==[r1.statement(g) for g in required] for o in row['candidates'])
    expected_candidates = {
        'TRANSPORT':has('ROOT','finite cyclic presentation transported by proved suspension isomorphism',transport),
        'TYPED_ISO':has('TYPED_ISO',ISO_RULE,(generic,)),
        'GENERIC_ISO':has('GENERIC_ISO','generic injective and surjective imply isomorphism',(inj,surj)),
        'DELTA_ZERO':has('DELTA_ZERO',ZERO_RULE,finite_cyclic_delta_zero_inputs(delta,domain)),
    }
    return {'sources_and_prior_eligibility':sources, 'expected_candidates':expected_candidates,
            'goals':rows, 'root_ancestor_count':len(root_scope),
            'root_given_nodes':[nodes[i] for i in sorted(root_scope) if nodes[i]['rule']=='GIVEN'],
            'root_inference_rules':[nodes[i]['inference_rule'] for i in sorted(root_scope) if nodes[i]['rule']=='INFERENCE'],
            'probe_policy':'POST_SEARCH_CANDIDATES_ONLY_NOT_PROOFS'}


def observe_worker(folder):
    from phase178_r1_k6_source_first_audit import audit as r1
    import phase165_r52_r9_shared_math as shared
    import phase165_r52_r2_search_adapter as adapter
    invocations = []

    def capture(real):
        def observed(*args, **kwargs):
            if (kwargs.get('n'),kwargs.get('k')) == (7,6):
                invocations.append(dict(kwargs))
            return real(*args,**kwargs)
        return observed
    with patch.object(shared,'search_registered_partial_proof',capture(shared.search_registered_partial_proof)), \
         patch.object(adapter,'search_registered_partial_proof',capture(adapter.search_registered_partial_proof)):
        summary = r1.observe(7,6,folder)
    require(len(invocations)==1,'ACTIVE_SEARCH_CONTEXT_COUNT:'+str(len(invocations)))
    detail = json.loads(Path(summary['detail']).read_text(encoding='utf-8'))
    result = {'summary':summary,'analysis':summarize(summary,detail),
              'probes':probe_active_context(invocations[0],summary,detail)}
    store(folder/'observation.json',result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    parser.add_argument('--timeout',type=int,default=180)
    parser.add_argument('--worker',action='store_true')
    parser.add_argument('--folder',type=Path)
    args = parser.parse_args()
    if args.worker:
        require(args.folder is not None and args.folder.is_dir(),'WORKER_FOLDER_REQUIRED')
        observe_worker(args.folder)
        return 0
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    base.mkdir(parents=True,exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_',dir=base))
    report = {'gate':'FAIL_R24','dry_run':args.dry_run,'full_pytest':'NOT_RUN'}
    try:
        from phase178_r1_k6_source_first_audit import audit as r1
        require(args.timeout>0,'POSITIVE_TIMEOUT_REQUIRED')
        report['preflight'] = preflight(r1)
        before = r1.snapshot()
        emit('HEAD',report['preflight']['head'])
        emit('SOURCE_CLAUSES','VERIFIED_ADOPTED_TRANSCRIPTION')
        if args.dry_run:
            report['gate'] = 'PASS_R24_DRYRUN'
        else:
            subprocess.run([sys.executable,'-B','-m',PACKAGE+'.audit','--worker','--folder',str(folder)],
                           cwd=ROOT,check=True,timeout=args.timeout)
            observation = json.loads((folder/'observation.json').read_text(encoding='utf-8'))
            report['observation'] = observation
            summary = observation['summary']
            for key in ('status','proven_step_count','open_goal_count','reference_count','trust_status','target_given_count','web_key'):
                emit('PUBLIC_'+key.upper(),summary[key])
            probes = observation['probes']
            emit('SOURCES_AND_PRIORS',json.dumps(probes['sources_and_prior_eligibility'],ensure_ascii=False))
            emit('EXPECTED_CANDIDATES',json.dumps(probes['expected_candidates'],ensure_ascii=False))
            emit('ROOT_ANCESTOR_COUNT',probes['root_ancestor_count'])
            emit('ROOT_GIVEN_COUNT',len(probes['root_given_nodes']))
            for row in probes['goals']:
                emit('PROBE',json.dumps({k:row[k] for k in ('name','actual_provider_visits','actual_tree_node_ids','root_ancestor_ids','linked_fixed_given_count','candidate_count')},ensure_ascii=False))
            for row in observation['analysis']['frontier']:
                emit('FRONTIER',json.dumps(row,ensure_ascii=False))
            detail = json.loads(Path(summary['detail']).read_text(encoding='utf-8'))
            for line in detail['web']['rendered_lines']:
                print(line)
            command = [sys.executable,'-B','-m','pytest','-q','-s','--import-mode=importlib','-p','no:cacheprovider',*TESTS]
            report['focused_command'] = command
            subprocess.run(command,cwd=ROOT,check=True)
            report['gate'] = ('PASS_R24_N7_VERIFIED_COMPLETE' if observation['analysis']['root_complete']
                              else 'PASS_R24_N7_SOURCE_FIRST_AUDIT_OPEN')
        require(r1.snapshot()==before,'REPOSITORY_CHANGED_DURING_AUDIT')
        require(preflight(r1)==report['preflight'],'POST_AUDIT_INTEGRITY_FAILED')
    except Exception as exc:
        report.update(gate='FAIL_R24',error=repr(exc),traceback=traceback.format_exc())
        emit('ERROR',repr(exc))
    store(folder/'report.json',report)
    emit('REPORT',folder/'report.json')
    emit('NEW_MATH_RULES',0)
    emit('NEW_GIVEN',0)
    emit('PROVIDER_CHANGED','NO')
    emit('RENDERER_CHANGED','NO')
    emit('HISTORICAL_GUARD','NOT_RUN_KNOWN_OPEN')
    emit('FULL_PYTEST','NOT_RUN')
    emit('GATE',report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())

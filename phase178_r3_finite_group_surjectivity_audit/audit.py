"""Inspect the real n=3,k=6 provider without adding inference rules or leaves."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback
from unittest.mock import patch

from phase178_r1_k6_source_first_audit.audit import (
    ROOT, blob_matches, git, git_text, require, snapshot, statement, store,
)

HEAD = '98ecbb664d5b2baf3eb5c20727ae54a078edbf78'
PACKAGE = Path(__file__).resolve().parent.name
PREFIX = 'PHASE178_R3_'
PINS = {
    'phase178_r1_k6_source_first_audit/audit.py': '4990d6ab37de46860a375d4d7a17207ed2daeb05',
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
    'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314',
    'phase165_r55_nk_only_goal.py': 'e436879f578148fe5c30f5a34974bea3425108b2',
    'phase165_r52_r9_shared_math.py': 'f4383a0c248fe62903203d1863df345740581c59',
    'phase165_r52_r2_search_adapter.py': 'c1d08b803a4d9f9e4e1ad5180a1487422f1cd191',
    'phase165_r14_r6_generic_iso.py': '8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7',
    'map_property_rules.py': '4adeebc9dedb3daf210cd8755be811aca32f1e8b',
    'phase165_r12_r12_ehp_consequences.py': '895dc98ad4d25f14fb7aac8fa52460a77fd049bc',
    'phase175_r4r12r13r4_hopf_zero_public/rule.py': '74b7e8dee9032f5b0cbfc0086646bb423e73be74',
    'phase171_r2j_r4_r6_middle_cardinality/source.py': '5df4d3e247d1e3f9a578dd4fc9e7434c3d3f62eb',
    'phase177_r15_finite_cyclic_delta_injective_public/provider.py': 'd22833c2ee5ad7c54c7690436e608e225c61a6e0',
    'phase177_r14_finite_cyclic_delta_injective_isolated/rule.py': 'fba57005273dfdf795501df5f71b3822f4ecddfe',
    'phase169_r10e4_ordered_db_prior/db_prior.py': '2ff19f92e10608f210fdb5fd3718f9ef9c71d91d',
    'phase176_r3r46r1_prior_group_availability/provider.py': 'dda7ac9fb93a60f94631e1a7b0cdf416dbb9cc33',
    'phase175_r3r9_lemma57_explicit_public/source.py': '0dbd07c4dbca7e3b3fcbbabf94126e111e21b1ab',
    'phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py': '66407339808ed4ba8a65c04fd3bfbbf05bde6745',
    'phase175_r4r12r13r4_hopf_zero_public/tests/test_rule.py': '44f8c403e6663569f1ff7d6eb1799d825911a4ab',
    'phase171_r2j_r4_r6_middle_cardinality/tests/test_audit.py': 'd9ffa7934e6c13259fbade74812b8c321c9264b4',
    'phase177_r14_finite_cyclic_delta_injective_isolated/tests/test_rule.py': '385c4daaa7c43ac74082e20e314235144addd427',
    'phase177_r15_finite_cyclic_delta_injective_public/tests/test_public.py': '8f6d2419933f3748a40749cbbdc3c65f4228fa24',
    'phase174_r3_r7_r6_cyclic_generator_zero_image/tests/test_rule.py': '5719b1ad79cd4a08057f2c0a5327dee196c3c199',
}
TESTS = (
    'phase175_r4r12r13r4_hopf_zero_public/tests/test_rule.py::test_two_backward_expansions_are_visible',
    'phase175_r4r12r13r4_hopf_zero_public/tests/test_rule.py::test_surjectivity_rule_accepts_only_zero_map_and_exactness',
    'phase171_r2j_r4_r6_middle_cardinality/tests/test_audit.py::test_generic_cardinality_product_without_middle_group_presentation',
    'phase171_r2j_r4_r6_middle_cardinality/tests/test_audit.py::test_bad_end_group_coordinates_and_fake_cardinality_are_rejected',
    'phase177_r14_finite_cyclic_delta_injective_isolated/tests/test_rule.py::test_conditional_chain',
    'phase177_r15_finite_cyclic_delta_injective_public/tests/test_public.py::test_generic_candidates',
    'phase174_r3_r7_r6_cyclic_generator_zero_image/tests/test_rule.py::test_two_proved_premises_derive_zero_image_and_keep_ancestors',
    'phase174_r3_r7_r6_cyclic_generator_zero_image/tests/test_rule.py::test_wrong_sphere_or_non_suspension_map_yields_no_candidate',
)


def emit(key, value):
    print(PREFIX + key + '=' + str(value), flush=True)


def preflight():
    require(Path(os.fsdecode(git('rev-parse', '--show-toplevel').strip())).resolve() == ROOT, 'WRONG_ROOT')
    require(git_text('branch', '--show-current') == 'develop', 'DEVELOP_REQUIRED')
    require(git_text('rev-parse', 'HEAD') == git_text('rev-parse', 'origin/develop') == HEAD, 'REVIEWED_HEAD_REQUIRED:'+HEAD)
    require(not git('status', '--porcelain', '--untracked-files=no'), 'TRACKED_WORKTREE_NOT_CLEAN')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    git('diff', '--check')
    for name, pin in PINS.items():
        require(git_text('rev-parse', 'HEAD:'+name) == pin and blob_matches(ROOT/name, pin), 'SOURCE_PIN_CHANGED:'+name)
    source = (ROOT/'sources/toda/Toda_05_2.tex').read_text(encoding='utf-8-sig')
    start = r'\begin{proposition}\label{prop:5.11}'
    end = r'\begin{equation}\label{eq:5.13}'
    require(source.count(start) == source.count(end) == 1, 'SOURCE_ANCHORS_CHANGED')
    proof = source.split(start, 1)[1].split(end, 1)[0]
    require(r'E\pi_7^2=0' in proof and r'\Delta\) は同型' in proof, 'SOURCE_ROUTE_CHANGED')
    return {'head': HEAD, 'pins': PINS, 'search_scope': [[3,6]], 'source': 'adopted Toda transcription, not original edition'}


def describe_option(option):
    return {'rule': option.rule.name, 'subgoals': [statement(x) for x in option.subgoals]}


def inspect_public_context():
    import phase165_r55_nk_only_goal as entry
    import phase165_r52_r2_search_adapter as adapter
    from expression import Zero
    from homotopy_groups import (
        FiniteCyclicGroup, TodaDeltaMap, TodaEHPExactnessWindow,
        TodaHopfInvariantMap, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement,
        TodaSuspensionMap,
    )
    from map_facts import EHP_DELTA_MAP, EHP_E_MAP
    from map_property_rules import ImageZeroStatement
    from phase165_r12_r11_prop42_unified import prop42_exactness_indices
    from phase165_r14_r6_generic_iso import GeneratorImage, MapInjective, MapIsomorphism, MapSurjective
    from phase169_r10e4_ordered_db_prior.db_prior import admitted_prior_group_step, verified_db_step
    from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
    from phase175_r3r9_lemma57_explicit_public.source import TodaLemma57ExplicitNuPrimeZero
    from phase177_r15_finite_cyclic_delta_injective_public.provider import presentation_candidates
    from proof import ProofRule, Relation
    from toda_rules import TodaHopfInvariantZeroStatement, TodaProp42ExactnessStatement

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(9,3))
    a, b, c = TodaPrimaryGroup(9,5), TodaPrimaryGroup(7,2), TodaPrimaryGroup(8,3)
    d = TodaPrimaryGroup(8,2)
    delta = TodaDeltaMap(a,b)
    lower_e = TodaSuspensionMap(b,c)
    upper_e = TodaSuspensionMap(d,root.group)
    exact = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(a,b,c,EHP_DELTA_MAP,EHP_E_MAP))
    require(prop42_exactness_indices(exact) == (2,8,'delta_e'), 'INVALID_EXPECTED_WINDOW')
    calls = []
    real = adapter.search_registered_partial_proof

    def observed(*args, **kwargs):
        require((kwargs.get('n'), kwargs.get('k')) == (3,6), 'UNEXPECTED_SEARCH_COORDINATES')
        calls.append(dict(kwargs))
        return real(*args, **kwargs)

    # One real root search, with no substituted result or modified provider.
    with patch.object(adapter, 'search_registered_partial_proof', observed):
        result = entry.search_group_from_registered_goal(n=3,k=6)
    require(len(calls) == 1 and result.target == root.group, 'PUBLIC_CONTEXT_CAPTURE_FAILED')
    invocation = calls[0]
    require(invocation['goal'] == root, 'ROOT_CHANGED')
    bridge = invocation['bridge']
    provider = invocation['expansion_provider']
    rows, claims = {}, {}
    for key, group in (('delta_domain',a),('delta_codomain',b),('upper_E_domain',d)):
        prior = admitted_prior_group_step(group, proof_target=root, bridge=bridge)
        require(prior is not None and verified_db_step(prior,proof_target=root,bridge=bridge), 'PRIOR_NOT_ADMITTED:'+key)
        claim = prior.conclusion
        require(type(claim) is Relation and claim.lhs == group and type(claim.rhs) is FiniteCyclicGroup and claim.rhs.order == 2, 'REVIEWED_PRIOR_SHAPE_CHANGED:'+key)
        claims[key] = claim
        rows[key] = {'claim':statement(claim),'order':claim.rhs.order,'provenance':str(prior.inference_rule.literature_reference),
                     'verified_adopted_db_prior':True,'public_presentation_candidates':[statement(x) for x in presentation_candidates(group,bridge=bridge,proof_target=root)]}
    sources = []
    for link in bridge.proof_links:
        step = link.step
        if step is None or step.rule is not ProofRule.GIVEN:
            continue
        if type(step.conclusion) is TodaLemma57ExplicitNuPrimeZero:
            ref = bridge.registry.reference(bridge.registry.assertion(link.assertion_id).reference_id)
            sources.append({'assertion_id':link.assertion_id,'locator':ref.locator,'conclusion':statement(step.conclusion)})
        require(step.conclusion != root, 'ROOT_GIVEN_PRESENT')
    require(len(sources)==1,'SCREENED_LEMMA57_EXPLICIT_CLAUSE_MISSING_OR_AMBIGUOUS')
    goals = {
        'delta_injective': MapInjective(delta),
        'delta_surjective': MapSurjective(delta),
        'delta_isomorphism': MapIsomorphism(delta),
        'delta_domain_cardinality': FiniteGroupCardinality(a,2),
        'delta_codomain_cardinality': FiniteGroupCardinality(b,2),
        'delta_E_exactness': exact,
        'lower_E_zero_image': ImageZeroStatement(lower_e),
        'lower_E_generator_zero': GeneratorImage(lower_e,claims['delta_codomain'].rhs.generator,Zero()),
        'upper_E_zero_image': ImageZeroStatement(upper_e),
        'upper_E_generator_zero': GeneratorImage(upper_e,claims['upper_E_domain'].rhs.generator,Zero()),
        'H_zero': TodaHopfInvariantZeroStatement(TodaHopfInvariantMap(root.group,a)),
        'upper_E_surjective': MapSurjective(upper_e),
        'root': root,
    }
    probes = {}
    for key, goal in goals.items():
        options = tuple(provider(goal))
        probes[key] = {'goal':statement(goal),'candidate_count':len(options),'options':[describe_option(x) for x in options]}
        emit('PROBE',json.dumps({'name':key,'candidate_count':len(options),'rules':[x.rule.name for x in options]},ensure_ascii=False))
    # These probes inspect immediate proposals, not completed independent proofs.
    return {'root_status':result.status.value,'root_open_goals':[statement(x) for x in result.open_goals],
            'root_step_count':len(result.proven_steps),'diagnostics':list(result.diagnostics),
            'prior_groups':rows,'lemma57_sources':sources,'probes':probes,
            'single_root_search':True,'probe_scope':'immediate candidates only, not derived proofs'}


def execute(dry_run):
    folder_base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    folder_base.mkdir(parents=True,exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_',dir=folder_base))
    report = {'phase':'178_R3','dry_run':dry_run,'gate':'FAIL_R3','full_pytest':'NOT_RUN','new_rules':0,'new_given':0}
    try:
        before = snapshot()
        report['preflight'] = preflight()
        emit('HEAD',HEAD)
        if dry_run:
            report['gate'] = 'PASS_R3_READ_ONLY_DRYRUN'
        else:
            report['audit'] = inspect_public_context()
            emit('ROOT_STATUS',report['audit']['root_status'])
            emit('ADMITTED_PRIOR_ORDERS',json.dumps({k:v['order'] for k,v in report['audit']['prior_groups'].items()}))
            store(folder/'report.json',report)
            command = [sys.executable,'-B','-m','pytest','-q','--import-mode=importlib','-p','no:cacheprovider',*TESTS]
            report['focused_command'] = command
            with (folder/'focused_pytest.txt').open('w',encoding='utf-8') as log:
                proc = subprocess.run(command,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1'),stdout=log,stderr=subprocess.STDOUT)
            print((folder/'focused_pytest.txt').read_text(encoding='utf-8',errors='replace'),flush=True)
            report['focused_pytest_exit_code'] = proc.returncode
            require(proc.returncode==0,'FOCUSED_PYTEST_FAILED')
            report['gate'] = 'PASS_R3_FINITE_GROUP_FRONTIER_AUDIT'
        require(snapshot()==before,'REPOSITORY_CHANGED_DURING_AUDIT')
        report['repository_unchanged'] = True
    except BaseException as exc:
        report.update(gate='FAIL_R3',error=repr(exc),traceback=traceback.format_exc())
        emit('ERROR',repr(exc))
    store(folder/'report.json',report)
    emit('REPORT',folder/'report.json')
    emit('FULL_PYTEST','NOT_RUN')
    emit('GATE',report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    return execute(args.dry_run)


if __name__ == '__main__':
    raise SystemExit(main())

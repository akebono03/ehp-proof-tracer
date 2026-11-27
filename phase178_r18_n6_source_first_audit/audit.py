"""Read-only observation of the public n=6,k=6 proof and its active provider."""
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

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
HEAD = 'de51c804796aadb88a4228e1863b329e2031ebce'
PREFIX = 'PHASE178_R18_'
PINS = {
    'phase165_r52_r9_shared_math.py': '5b23a40f62069c00ae30bee6ed670d66f8a3daf9',
    'phase178_r1_k6_source_first_audit/audit.py': '4990d6ab37de46860a375d4d7a17207ed2daeb05',
    'phase178_r15_toda512_isolated/source.py': 'c0dedf1aa758adf6f7f925ea86ec7a85c5f994dc',
    'phase178_r15_toda512_isolated/provider.py': 'b7114fb01a851d0ad9a5a16ee794e4ec603b7d50',
    'phase178_r15_toda512_isolated/source_contract.py': 'b712da395b5e399009c131ae3d3ea6044fcf69e2',
    'phase178_r16_toda513_isolated/source.py': '73300491e27c4d4298e07d8b0bd9c6653328b609',
    'phase178_r16_toda513_isolated/source_contract.py': '8e6aa8beac6bc3c5f490f64b262aaa83d33a829b',
    'phase165_r14_r6_generic_iso.py': '8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7',
    'phase165_r14_r9_ehp_exactness.py': 'c39759f0b693ce89100ef8439e8aec7fe325694f',
    'phase165_r14_r11_delta_zero.py': '0bc61ede969bb3ddf43cdd43e9ef7a557c4dac61',
    'phase165_r12_r24_web_search_connection.py': '71d0c6c365a46e833a2bfe304c771d2e010178ca',
    'phase165_r12_r12_ehp_consequences.py': '895dc98ad4d25f14fb7aac8fa52460a77fd049bc',
    'phase169_r10e1_general_group_transport/transport.py': '3865d1e57923a0d45f0240cc357110e51b20a3e1',
    'phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py': '66407339808ed4ba8a65c04fd3bfbbf05bde6745',
    'phase174_r3_r7_r40_adopted_db_zero_image_isolated/rule.py': 'dfa1519c629eef92ca1c5dae265acc050883649b',
    'phase175_r4r14r9_literature_zero_image/rule.py': '82d69284c16a3e77eacf1b23a4eb84a13249dd56',
    'phase176_r3r46r1_prior_group_availability/provider.py': 'dda7ac9fb93a60f94631e1a7b0cdf416dbb9cc33',
    'phase175_r4r12r13r2_delta_injective_e_surjective/rule.py': '763b98521f8d78bbca1f07944194384c55a9ed57',
    'phase175_r4r12r13r3_public_delta_e_bridge/provider.py': '17657b9eb278c020cf484f1a31d87aad7997e05b',
    'phase176_r3r48_cited_finite_delta_kernel/rule.py': '86cc4a468ffd4601337bbef589a37fa46b449263',
    'phase169_r10e4_ordered_db_prior/db_prior.py': '2ff19f92e10608f210fdb5fd3718f9ef9c71d91d',
    'phase174_r3_r7_r53_public_source_bound_kernel/provider.py': '2ccfea07d35975c7bc6e200e2c8eece47fb75f58',
    'phase169_r4c_pi64_suspension_iso/rule.py': 'c5cc2190d243997fccb11751f5d530bf8fc12085',
    'phase178_r17r3_common_renderer/projection.py': '1e9ae1648f5b8e8d249c91d925934ade88082843',
    'phase178_r17r3_common_renderer/tests/test_display.py': '934fcdec3976b45e7e9570a780a47adca6837cca',
    'phase178_r16_toda513_isolated/tests/test_registration.py': 'b16cbb51c8f7463237b7e31458cb8205041a993e',
    'phase178_r17r2_cited_512_priority/tests/test_priority.py': '7e9af427d78dd37793ec3014db1bb167fc1319a9',
    'phase175_r4r12r13r3_public_delta_e_bridge/tests/test_provider.py': 'f568b9591f3af50c524693f998183fd157ffcdb3',
    'phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py': '48bae67c01b6a22a21ec2b9e90255c07b4e53696',
    'phase171_r20r2_first_successful_search/tests/test_first_successful_search.py': 'bd37cb05011ed0d9413bdd7f7335a116d29dae33',
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
    'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314',
    'phase168_r3_41p13_trust_boundary/verification.py': '547464846ce574d227092a4aacb895d2e2dfefca',
}
TESTS = (
    PACKAGE + '/tests/test_audit.py',
    'phase178_r16_toda513_isolated/tests/test_registration.py',
    'phase178_r17r2_cited_512_priority/tests/test_priority.py',
    'phase175_r4r12r13r3_public_delta_e_bridge/tests/test_provider.py',
    'phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py',
    'phase171_r20r2_first_successful_search/tests/test_first_successful_search.py',
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print(PREFIX + key + '=' + str(value), flush=True)


def store(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + '\n', encoding='utf-8')


def preflight(r1):
    require(Path(os.fsdecode(r1.git('rev-parse', '--show-toplevel').strip())).resolve() == ROOT, 'WRONG_ROOT')
    require(r1.git_text('branch', '--show-current') == 'develop', 'DEVELOP_REQUIRED')
    head = r1.git_text('rev-parse', 'HEAD')
    require(head == r1.git_text('rev-parse', 'origin/develop') == HEAD, 'REVIEWED_HEAD_REQUIRED:' + HEAD)
    require(not r1.git('status', '--porcelain', '--untracked-files=no'), 'TRACKED_WORKTREE_NOT_CLEAN')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    for path, pin in PINS.items():
        require(r1.git_text('rev-parse', 'HEAD:' + path) == pin and r1.blob_matches(ROOT / path, pin), 'PIN_CHANGED:' + path)
    for path in TESTS:
        require((ROOT / path).is_file(), 'FOCUSED_TEST_MISSING:' + path)
    r1.git('diff', '--check')
    from phase178_r15_toda512_isolated.source_contract import verify_clause as verify_512
    from phase178_r16_toda513_isolated.source_contract import verify_clause as verify_513
    chapter = (ROOT / 'sources/toda/Toda_05_2.tex').read_text(encoding='utf-8-sig')
    return {'head': head, 'eq512_line': verify_512(chapter), 'eq513_line': verify_513(chapter)}


def summarize(summary, detail):
    """Report observed public frontier only; a proposal is never a proof."""
    require((summary['n'], summary['k']) == (6, 6), 'WRONG_TARGET')
    require(summary['status'] in ('complete', 'partial', 'search_failed', 'not_searched'), 'UNMEASURED_TARGET')
    require(summary['web_error'] is None and summary['web_key'] is not None, 'WEB_GAP')
    require(summary['target_given_count'] == 0, 'TARGET_GIVEN_FOUND')
    require(summary['complete_invariants_hold'], 'TRUST_CONTRACT_FAILED')
    require(len(detail['open_goals']) == summary['open_goal_count'], 'OPEN_GOAL_COUNT_CHANGED')
    inventory = detail['screened_source_inventory']
    require(inventory is not None and not inventory['target_group_given_links'], 'SCREENED_TARGET_GIVEN_OR_MISSING_CONTEXT')
    complete = summary['status'] == 'complete'
    if complete:
        require(summary['trust_status'] == 'VERIFIED' and summary['open_goal_count'] == 0
                and summary['web_key'] == 'generic-complete-proof', 'COMPLETE_NOT_VERIFIED')
    frontier = []
    for item in detail['frontier']:
        frontier.append({'goal': item['goal'], 'state': item['state'],
                         'rules': list(dict.fromkeys(o['rule'] for batch in item['observed_expansions'] for o in batch['options']))})
    return {'root_complete': complete, 'frontier': frontier,
            'provider_call_count': len(detail['provider_calls']),
            'search_context': detail['search_context'], 'screened_source_inventory': inventory}


def probe_active_context(invocation, detail):
    """Inspect typed candidate availability after the real search has returned.

    No candidate is applied. No additional proof search or GIVEN admission is
    performed by this diagnostic; the DB admission API is queried for eligibility.
    """
    from homotopy_groups import (FiniteCyclicGroup, TodaPrimaryGroup, TodaDeltaMap,
                                  TodaSuspensionMap, TodaSuspensionIsomorphismStatement,
                                  TodaEHPExactnessWindow)
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r14_r6_generic_iso import GeneratorImage, MapInjective, MapSurjective, MapIsomorphism
    from map_property_rules import ImageZeroStatement, KernelZeroStatement, InjectiveMapStatement
    from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
    from toda_rules import TodaDeltaZeroStatement, TodaProp42ExactnessStatement
    from phase178_r15_toda512_isolated.source import canonical_512
    from phase178_r16_toda513_isolated.source import canonical_513
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result, admitted_prior_group_step
    from phase176_r3r48_cited_finite_delta_kernel.rule import linked_cited_steps
    from proof import Relation
    from phase178_r1_k6_source_first_audit import audit as r1

    root, bridge, provider = (invocation[k] for k in ('goal', 'bridge', 'expansion_provider'))
    expected = exact_prior_database_result(6, 6)
    require(type(root) is Relation and type(root.rhs) is FiniteCyclicGroup and root == expected
            and root.lhs == TodaPrimaryGroup(12, 6) and root.rhs.order == 2, 'ROOT_PRESENTATION_CHANGED')
    middle, db_source = exact_prior_database_result(5, 6), exact_prior_database_result(11, 2)
    require(type(middle) is Relation and type(middle.rhs) is FiniteCyclicGroup and middle.lhs == TodaPrimaryGroup(11, 5), 'PREVIOUS_STEM_ROW_MISSING')
    source_512, source_513 = canonical_512(5), canonical_513()[1]
    c = TodaPrimaryGroup(13, 11)
    # The expected presentation is a diagnostic goal, not an admitted fact.
    source = Relation(c, FiniteCyclicGroup(2, source_513.source_generator))
    a, b = middle.lhs, root.lhs
    htarget, dtarget = TodaPrimaryGroup(12, 11), TodaPrimaryGroup(10, 5)
    lower_delta, suspension = TodaDeltaMap(c, a), TodaSuspensionMap(a, b)
    require(source_512.statement == MapInjective(TodaDeltaMap(htarget, dtarget)) and source_513.map == lower_delta, 'SOURCE_MAP_CHANGED')
    delta_e = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(source_term=c, middle_term=a, target_term=b, first_map=EHP_DELTA_MAP, second_map=EHP_E_MAP))
    e_h = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(source_term=a, middle_term=b, target_term=htarget, first_map=EHP_E_MAP, second_map=EHP_H_MAP))
    h_delta = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(source_term=b, middle_term=htarget, target_term=dtarget, first_map=EHP_H_MAP, second_map=EHP_DELTA_MAP))
    image = GeneratorImage(suspension, middle.rhs.generator, root.rhs.generator)
    targets = (
        ('ROOT_RELATION', root),
        ('ROOT_CYCLIC_STRUCTURE', CyclicStructureStatement(b, root.rhs.generator, root.rhs.order)),
        ('E_TODA_ISOMORPHISM', TodaSuspensionIsomorphismStatement(suspension)),
        ('E_GENERIC_ISOMORPHISM', MapIsomorphism(suspension)),
        ('E_INJECTIVE', MapInjective(suspension)),
        ('E_ALTERNATE_INJECTIVE', InjectiveMapStatement(suspension)),
        ('E_ZERO_KERNEL', KernelZeroStatement(suspension)),
        ('DELTA_ZERO_IMAGE', ImageZeroStatement(lower_delta)),
        ('DELTA_ZERO_TODA', TodaDeltaZeroStatement(lower_delta)),
        ('DELTA_GENERATOR_ZERO', source_513),
        ('DELTA_DOMAIN_GROUP', source),
        ('DELTA_E_EXACT', delta_e),
        ('E_SURJECTIVE', MapSurjective(suspension)),
        ('UPPER_DELTA_INJECTIVE', source_512.statement),
        ('CITED_512_LEAF', source_512),
        ('H_DELTA_EXACT', h_delta),
        ('E_H_EXACT', e_h),
        ('PRIOR_STEM_GROUP', middle),
        ('E_GENERATOR_IMAGE', image),
    )
    rows = []
    for name, goal in targets:
        goal_data = r1.statement(goal)
        observed = [batch for batch in detail['provider_calls'] if batch['goal'] == goal_data]
        proved = [node['id'] for node in detail['tree']['nodes'] if node['conclusion'] == goal_data]
        direct = linked_cited_steps(bridge, goal)
        options = provider(goal)
        rows.append({'name': name, 'goal': goal_data, 'actual_provider_visits': len(observed),
                     'actual_tree_node_ids': proved, 'linked_fixed_given_count': len(direct),
                     'candidate_count': len(options),
                     'candidates': [{'rule': opt.rule.name, 'subgoals': [r1.statement(g) for g in opt.subgoals]} for opt in options]})
    prior_checks = {}
    for label, statement in (('DELTA_DOMAIN', source), ('PREVIOUS_STEM', middle)):
        prior = admitted_prior_group_step(statement.lhs, proof_target=root, bridge=bridge)
        prior_checks[label] = {'eligible': prior is not None and prior.conclusion == statement,
                               'presentation': r1.statement(statement), 'order': statement.rhs.order}
    sources = {'512_screened_link_count': len(linked_cited_steps(bridge, source_512)),
               '513_screened_link_count': len(linked_cited_steps(bridge, source_513)),
               'delta_domain_db_presentation': r1.statement(db_source) if db_source is not None else None,
               '513_generator_matches_db': (type(db_source) is Relation and type(db_source.rhs) is FiniteCyclicGroup
                                            and source_513.source_generator == db_source.rhs.generator),
               'delta_domain_db_matches_expected': db_source == source,
               'previous_stem_order_matches_root': middle.rhs.order == root.rhs.order,
               'prior_checks': prior_checks}
    return {'sources_and_prior_eligibility': sources, 'goals': rows,
            'probe_policy': 'POST_SEARCH_CANDIDATES_ONLY_NOT_PROOFS'}


def observe_worker(folder):
    """Capture the active screened context without changing the search provider."""
    from phase178_r1_k6_source_first_audit import audit as r1
    import phase165_r52_r9_shared_math as shared
    import phase165_r52_r2_search_adapter as adapter

    invocations = []

    def capture(real):
        def observed(*args, **kwargs):
            if (kwargs.get('n'), kwargs.get('k')) == (6, 6):
                invocations.append(dict(kwargs))
            return real(*args, **kwargs)
        return observed

    with patch.object(shared, 'search_registered_partial_proof', capture(shared.search_registered_partial_proof)), \
         patch.object(adapter, 'search_registered_partial_proof', capture(adapter.search_registered_partial_proof)):
        summary = r1.observe(6, 6, folder)
    require(len(invocations) == 1, 'ACTIVE_SEARCH_CONTEXT_COUNT:' + str(len(invocations)))
    detail = json.loads(Path(summary['detail']).read_text(encoding='utf-8'))
    analysis = summarize(summary, detail)
    probes = probe_active_context(invocations[0], detail)
    report = {'summary': summary, 'analysis': analysis, 'probes': probes}
    store(folder / 'observation.json', report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--timeout', type=int, default=180)
    parser.add_argument('--worker', action='store_true')
    parser.add_argument('--folder', type=Path)
    args = parser.parse_args()
    if args.worker:
        require(args.folder is not None and args.folder.is_dir(), 'WORKER_FOLDER_REQUIRED')
        observe_worker(args.folder)
        return 0
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))
    report = {'gate': 'FAIL_R18', 'dry_run': args.dry_run, 'new_rules': 0, 'new_given': 0, 'full_pytest': 'NOT_RUN'}
    try:
        from phase178_r1_k6_source_first_audit import audit as r1
        require(args.timeout > 0, 'POSITIVE_TIMEOUT_REQUIRED')
        before = r1.snapshot()
        report['preflight'] = preflight(r1)
        emit('HEAD', HEAD)
        emit('SOURCE_CLAUSES', 'VERIFIED_ADOPTED_TRANSCRIPTION')
        if args.dry_run:
            report['gate'] = 'PASS_R18_READ_ONLY_DRYRUN'
        else:
            subprocess.run([sys.executable, '-B', '-m', PACKAGE + '.audit', '--worker', '--folder', str(folder)],
                           cwd=ROOT, check=True, timeout=args.timeout)
            observation = json.loads((folder / 'observation.json').read_text(encoding='utf-8'))
            report['observation'] = observation
            summary = observation['summary']
            for key in ('status', 'proven_step_count', 'open_goal_count', 'reference_count', 'trust_status', 'target_given_count', 'web_key'):
                emit('PUBLIC_' + key.upper(), summary[key])
            for item in observation['analysis']['frontier']:
                emit('FRONTIER', json.dumps(item, ensure_ascii=False))
            emit('SOURCES_AND_PRIORS', json.dumps(observation['probes']['sources_and_prior_eligibility'], ensure_ascii=False))
            for row in observation['probes']['goals']:
                emit('PROBE', json.dumps({'name': row['name'], 'actual_provider_visits': row['actual_provider_visits'],
                                          'actual_tree_node_ids': row['actual_tree_node_ids'], 'linked_fixed_given_count': row['linked_fixed_given_count'],
                                          'candidate_count': row['candidate_count'],
                                          'rules': [item['rule'] for item in row['candidates']]}, ensure_ascii=False))
            command = [sys.executable, '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider', '--import-mode=importlib', *TESTS]
            report['focused_command'] = command
            subprocess.run(command, cwd=ROOT, check=True)
            report['gate'] = 'PASS_R18_N6_SOURCE_FIRST_AUDIT'
        require(r1.snapshot() == before, 'REPOSITORY_CHANGED_DURING_AUDIT')
        report['repository_unchanged'] = True
    except Exception as exc:
        report.update(gate='FAIL_R18', error=repr(exc), traceback=traceback.format_exc())
        emit('ERROR', repr(exc))
    store(folder / 'report.json', report)
    emit('REPORT', folder / 'report.json')
    emit('NEW_MATH_RULES', 0)
    emit('NEW_GIVEN', 0)
    emit('FULL_PYTEST', 'NOT_RUN')
    emit('GATE', report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())

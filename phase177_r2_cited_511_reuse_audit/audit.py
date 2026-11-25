"""Observe (5.11) reuse and the unsigned Delta composition frontier."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
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
HEAD = '45d648fab515d1a7d2f48c4a411933926d9d57e9'
PINS = {
    'phase165_r52_r9_shared_math.py': '87e0fe1202fa265c7530d0dd7e2b0adda2f5ebc2',
    'phase165_r55_nk_only_goal.py': 'e436879f578148fe5c30f5a34974bea3425108b2',
    'phase165_r3_recursive_search.py': '34c63d520eb102d0d1e6340148f9b7a1dd9eaace',
    'web_group_proof.py': '2c66da9c8e80a13812a63b6adda34c9414d8413c',
    'phase175_r4r12r10r1_cited_511_public/source.py': '92670af82d86c0a22b77ddde3b6d6ceb3ac17e5a',
    'phase175_r4r12r10r1_cited_511_public/provider.py': '6a57c443d8c69192ba58e213821cb62aac37553f',
    'phase175_r4r10_cited_58_prop25_public/source.py': 'b5162bdaac25e4578973816290207379734229f6',
    'phase175_r4r10_cited_58_prop25_public/provider.py': 'be1d726fe98c0258685674ea41099aab1103f318',
    'phase175_r4r7_prop25_typed_composition/rule.py': 'e957752baf93f75352d106e53205730af9a02b4d',
    'phase175_r4r12_public_two_summand_quotient/provider.py': '1b34fe0d2707a51af7acc52eaa7d38209e90dfa2',
    'phase175_r4r12r9_delta_generator_image_bridge/rule.py': 'cfff81f4662825b78f30f8b7b4886cb27333b6c2',
    'phase175_r4r12r13r2_delta_injective_e_surjective/rule.py': '763b98521f8d78bbca1f07944194384c55a9ed57',
    'phase168_r2_8_3_generator_identity/identity.py': '9052b3d75809a4a45e026d93da80f6d4aaad8b62',
    'sources/toda/Toda_02_2.tex': 'ed3667788805a429140dedf5d183736e43e0f2c3',
    'sources/toda/Toda_05_2.tex': '579661138928499ba04a51327f686d9b971b5314',
    'data/sphere.csv': 'b7e98a4469e0dcf2c5ea16691a7225951fd36395',
}


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, encoding='utf-8').strip()


def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()


def matches_blob(raw, pin):
    lf = raw.replace(b'\r\n', b'\n')
    return pin in (blob(raw), blob(lf), blob(lf.replace(b'\n', b'\r\n')))


def snapshot():
    return (git('rev-parse', 'HEAD'), git('diff', '--binary', 'HEAD'),
            git('diff', '--cached', '--binary'), git('status', '--porcelain', '--untracked-files=all'))


def preflight():
    if Path(git('rev-parse', '--show-toplevel')).resolve() != ROOT:
        raise RuntimeError('WRONG_REPOSITORY_ROOT')
    if git('branch', '--show-current') != 'develop':
        raise RuntimeError('DEVELOP_REQUIRED')
    local_head = git('rev-parse', 'HEAD')
    remote_head = git('rev-parse', 'origin/develop')
    if local_head != HEAD or remote_head != HEAD:
        raise RuntimeError(
            f'REVIEWED_HEAD_REQUIRED:expected={HEAD};local={local_head};origin/develop={remote_head}'
        )
    if git('status', '--porcelain', '--untracked-files=no'):
        raise RuntimeError('TRACKED_WORKTREE_NOT_CLEAN')
    for name, pin in PINS.items():
        if git('rev-parse', 'HEAD:' + name) != pin or not matches_blob((ROOT/name).read_bytes(), pin):
            raise RuntimeError('SOURCE_PIN_CHANGED:' + name)
    from phase175_r4r12r10r1_cited_511_public.source import verify_cited_511
    from phase175_r4r10_cited_58_prop25_public.source import source_positions
    positions = source_positions(ROOT)
    positions['toda:(5.11)'] = verify_cited_511(ROOT)
    if not positions['toda:Proposition 2.5'] < positions['toda:(5.11)']:
        raise RuntimeError('SOURCE_ORDER_INVALID')
    return {'head': HEAD, 'source_positions': positions, 'pins': PINS}


def option_records(options):
    return [{'rule': o.rule.name, 'subgoals': [repr(g) for g in o.subgoals]} for o in options]


def matching_calls(goal, calls):
    return [option_records(options) for requested, options in calls
            if type(requested) is type(goal) and requested == goal]


def classify_calls(batches):
    if not batches:
        return 'NOT_REACHED'
    return 'CANDIDATES_PRESENT' if any(batches) else 'NO_CANDIDATES'


def capture():
    import phase165_r55_nk_only_goal as entry
    import phase165_r52_r9_shared_math as shared
    import phase165_r52_r3_web_adapter as web_adapter
    from web_group_proof import build_standard_web_group_proof_view

    real_entry = entry.search_group_from_registered_goal
    real_adapter = shared.search_registered_partial_proof
    real_web = web_adapter.build_partial_web_group_proof_view
    invocations, results, calls, models = [], [], [], []

    def observed_entry(*args, **kwargs):
        result = real_entry(*args, **kwargs)
        results.append(result)
        return result

    def observed_adapter(*args, **kwargs):
        if (kwargs.get('n'), kwargs.get('k')) != (5, 5):
            return real_adapter(*args, **kwargs)
        invocations.append(dict(kwargs))
        provider = kwargs['expansion_provider']

        def observed_provider(goal):
            options = provider(goal)
            calls.append((goal, options))
            return options

        return real_adapter(*args, **dict(kwargs, expansion_provider=observed_provider))

    def observed_web(result, **kwargs):
        models.append((result, kwargs.get('narrative_model')))
        return real_web(result, **kwargs)

    with patch.object(entry, 'search_group_from_registered_goal', observed_entry), \
         patch.object(shared, 'search_registered_partial_proof', observed_adapter), \
         patch.object(web_adapter, 'build_partial_web_group_proof_view', observed_web):
        view = build_standard_web_group_proof_view(n=5, k=5, max_depth=2,
                                                   mode='narrative', citation_source='model')
    if len(invocations) != 1 or len(results) != 1 or len(models) != 1 or models[0][0] is not results[0]:
        raise RuntimeError('PUBLIC_CAPTURE_MISMATCH')
    return invocations[0], results[0], tuple(calls), models[0][1], view


def source_records(bridge, claim):
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin
    rows = []
    for link in bridge.proof_links:
        step = link.step
        if step is None or type(step.conclusion) is not type(claim) or step.conclusion != claim:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        reference = bridge.registry.reference(assertion.reference_id)
        rows.append({'assertion_id': link.assertion_id, 'locator': reference.locator,
                     'position': reference.publication_position,
                     'eligible_fixed_given': (step.rule is ProofRule.GIVEN and not step.premises
                                              and assertion.origin is AssertionOrigin.FIXED_STATEMENT
                                              and assertion.content == claim)})
    return rows


def replay_source(goal, invocation):
    """Independent DFS, not evidence accepted by the actual root search."""
    from phase165_r3_recursive_search import reconstruct_registered_goal, RegisteredGoalUnresolved
    calls = []
    provider = invocation['expansion_provider']

    def observed(target):
        options = provider(target)
        calls.append({'goal': repr(target), 'options': option_records(options)})
        return options

    try:
        step = reconstruct_registered_goal(
            goal, invocation['bridge'], invocation['citing_assertion_id'], observed,
            lookup_mode=invocation['lookup_mode'],
            verified_assertion_ids=invocation.get('verified_assertion_ids', ()),
            completed_internal_proofs=invocation.get('completed_internal_proofs', ()),
        )
    except RegisteredGoalUnresolved as exc:
        return {'proved': False, 'error': str(exc), 'calls': calls}
    if type(step.conclusion) is not type(goal) or step.conclusion != goal:
        raise RuntimeError('SOURCE_REPLAY_WRONG_CONCLUSION')
    return {'proved': True, 'trust': step.rule.name,
            'inference_rule': step.inference_rule.name if step.inference_rule else None,
            'calls': calls}


def arithmetic(m, i, j):
    return (all(type(x) is int for x in (m, i, j)) and m >= 2 and i >= 2*m
            and j >= i and (m % 2 == 1 or j < 3*m-1))


def observe():
    from expression import Composition, GeneratorSymbol, HomotopyElement, IteratedSuspension, MapApplication
    from map_facts import EHP_DELTA_MAP
    from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
    from phase175_r4r10_cited_58_prop25_public.source import CitedTodaProp25
    from phase175_r4r10_cited_58_prop25_public.provider import screened_cited_facts, expand_cited_prop25
    from phase175_r4r12r10r1_cited_511_public.source import CitedToda511, canonical_511
    from phase175_r4r12r10r1_cited_511_public.provider import expand_cited_511
    from phase175_r4r12_public_two_summand_quotient.provider import expand_public_two_summand_quotient
    from phase175_r4r12r9_delta_generator_image_bridge.rule import delta_image_equality
    from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
    from phase168_r2_8_3_generator_identity.identity import _generator_identity, _master_records
    from proof import Relation

    invocation, result, calls, model, view = capture()
    root, bridge = invocation['goal'], invocation['bridge']
    if (result.target != TodaPrimaryGroup(10, 5) or root.lhs != result.target
            or result.status.value != 'partial' or view.key != 'generic-partial-proof'
            or not view.partial_result or model is None or result.conclusion is not None):
        raise RuntimeError('R1_PARTIAL_BASELINE_CHANGED_REQUIRES_REVIEW')
    base = canonical_511()
    claim, prop, definition = CitedToda511(base), CitedTodaProp25(), TodaEtaFamilyGeneralDefinition()
    available = screened_cited_facts(bridge)
    sources = {name: {'count': available.count(value), 'links': source_records(bridge, value)}
               for name, value in [('511', claim), ('prop25', prop), ('eta_definition', definition)]}
    if any(value['count'] != 1 or sum(r['eligible_fixed_given'] for r in value['links']) != 1
           for key, value in sources.items() if key in ('511', 'prop25')):
        source_state = 'SOURCE_NOT_UNIQUELY_AVAILABLE'
    else:
        source_state = 'BOTH_SOURCES_SCREENED'
    eta8 = HomotopyElement('η₈', 8, 9, 8, GeneratorSymbol('η', index=8))
    eta10 = HomotopyElement('η₁₀', 10, 11, 10, GeneratorSymbol('η', index=10))
    alpha, value = base.lhs.expression, base.rhs
    expanded = Relation(MapApplication(EHP_DELTA_MAP, Composition(alpha, IteratedSuspension(eta8, 2))),
                        Composition(value, eta8))
    canonical = Relation(MapApplication(EHP_DELTA_MAP, Composition(alpha, eta10)), Composition(value, eta8))
    suspension = Relation(IteratedSuspension(eta8, 2), eta10)
    if (typed_endpoints(alpha), typed_endpoints(eta8), typed_endpoints(value)) != ((10,9),(9,8),(8,4)) or not arithmetic(4,9,10):
        raise RuntimeError('CANONICAL_PROP25_PARAMETERS_INVALID')
    cyclic = CyclicStructureStatement(root.lhs, root.rhs.generator, 2)
    routes = expand_public_two_summand_quotient(cyclic, proof_target=root)
    if len(routes) != 2:
        raise RuntimeError('TWO_QUOTIENT_ROUTES_EXPECTED')
    records = _master_records()
    def identity(value):
        return _generator_identity(value, records)
    expected_rhs = identity(canonical.rhs)
    expected_lhs = identity(canonical.lhs.expression)
    route_rows, actual_goals = [], []
    for route in routes:
        image = route.subgoals[2]
        eq = delta_image_equality(image)
        if eq is None:
            raise RuntimeError('DELTA_IMAGE_NOT_TYPED')
        actual_goals.append(eq)
        batches = matching_calls(eq, calls)
        route_rows.append({'equation': repr(eq), 'image': repr(image),
                           'source_identity_matches': expected_lhs is not None and identity(eq.lhs.expression) == expected_lhs,
                           'target_identity_matches': expected_rhs is not None and identity(eq.rhs) == expected_rhs,
                           'actual_calls': batches, 'classification': classify_calls(batches),
                           'open': eq in result.open_goals, 'subgoals': [repr(g) for g in route.subgoals]})
    if not any(row['actual_calls'] for row in route_rows):
        raise RuntimeError('ACTUAL_DELTA_FRONTIER_NOT_OBSERVED')
    probes = [('base_511', base), ('explicit_double_suspension', expanded),
              ('canonical_composite', canonical), ('eta_double_suspension', suspension),
              ('next_delta_injective', MapInjective(TodaDeltaMap(TodaPrimaryGroup(10,9), TodaPrimaryGroup(8,4)))),
              ('suspension_surjective', MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(9,4), TodaPrimaryGroup(10,5))))]
    # Use the original provider after the root run. These are diagnostic proposals only.
    provider = invocation['expansion_provider']
    probe_rows = {name: {'goal': repr(goal), 'options': option_records(provider(goal)),
                         'actual_calls': matching_calls(goal, calls)} for name, goal in probes}
    base_replay = replay_source(base, invocation)
    prop_replay = replay_source(prop, invocation)
    expected_route = [row for row in route_rows if row['source_identity_matches'] and row['target_identity_matches']]
    unsigned_count = len(expand_cited_prop25(expanded, available))
    if (source_state != 'BOTH_SOURCES_SCREENED' or not base_replay['proved']
            or base_replay.get('trust') != 'INFERENCE' or not prop_replay['proved']
            or prop_replay.get('trust') != 'GIVEN'):
        diagnosis = 'SOURCE_REUSE_BLOCKED'
    elif len(expected_route) != 1:
        diagnosis = 'REGISTERED_COMPOSITE_IDENTITY_REQUIRES_REVIEW'
    elif unsigned_count == 0 and not probe_rows['explicit_double_suspension']['options'] and not probe_rows['canonical_composite']['options']:
        diagnosis = 'UNSIGNED_DELTA_COMPOSITION_FRONTIER'
    else:
        diagnosis = 'EXISTING_CANDIDATES_REQUIRE_REVIEW'
    return {'status': result.status.value, 'web_key': view.key, 'root': repr(root),
            'open_goals': [repr(g) for g in result.open_goals], 'open_goal_count': len(result.open_goals),
            'accepted_steps': [{'conclusion': repr(s.conclusion), 'trust': s.rule.name} for s in result.proven_steps],
            'citations': [repr(c) for c in model.citations], 'lookup_mode': invocation['lookup_mode'],
            'source_state': source_state, 'sources': sources, 'diagnosis': diagnosis,
            'arithmetic': {'m': 4, 'i': 9, 'j': 10, 'bound': 11, 'valid': True},
            'routes': route_rows, 'independent_probes_not_root_evidence': probe_rows,
            'base_511_isolated_options': option_records(expand_cited_511(base, available)),
            'existing_signed_prop25_unsigned_candidate_count': unsigned_count,
            'independent_source_replays_not_root_evidence': {'511': base_replay, 'prop25': prop_replay},
            'new_math_rules': 0, 'new_given_registrations': 0, 'full_pytest': 'NOT_RUN'}


def execute(dry_run):
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir())/'EHPProofTracerAudit'/PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))
    report = {'phase': '177_R2', 'dry_run': dry_run, 'full_pytest': 'NOT_RUN',
              'gate': 'FAIL_R2', 'utc': datetime.now(timezone.utc).isoformat()}
    try:
        before = snapshot()
        report['preflight'] = preflight()
        if not dry_run:
            report['observation'] = observe()
        if snapshot() != before:
            raise RuntimeError('REPOSITORY_CHANGED_DURING_AUDIT')
        report['repository_unchanged'] = True
        report['gate'] = 'PASS_R2_READ_ONLY_DRYRUN' if dry_run else 'PASS_R2_CITED_511_REUSE_AUDITED'
    except Exception as exc:
        report.update(error=repr(exc), traceback=traceback.format_exc())
    path = folder/'report.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    for key in ('status', 'web_key', 'open_goal_count', 'source_state', 'diagnosis', 'arithmetic',
                'existing_signed_prop25_unsigned_candidate_count'):
        if key in report.get('observation', {}):
            print('PHASE177_R2_'+key.upper()+'='+json.dumps(report['observation'][key], ensure_ascii=False))
    for name, value in report.get('observation', {}).get('independent_source_replays_not_root_evidence', {}).items():
        print('PHASE177_R2_REPLAY_'+name.upper()+'='+json.dumps(value['proved']))
    for row in report.get('observation', {}).get('routes', []):
        print('PHASE177_R2_ROUTE='+json.dumps({k:row[k] for k in ('source_identity_matches','target_identity_matches','classification','open')}, ensure_ascii=False))
    if 'error' in report:
        print('PHASE177_R2_ERROR='+report['error'])
    print('PHASE177_R2_REPORT='+str(path))
    print('PHASE177_R2_FULL_PYTEST=NOT_RUN')
    print('PHASE177_R2_GATE='+report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    return execute(parser.parse_args().dry_run)


if __name__ == '__main__':
    raise SystemExit(main())

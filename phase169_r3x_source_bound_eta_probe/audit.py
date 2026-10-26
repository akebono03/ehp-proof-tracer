"""Phase 169 R3X: prove the higher-eta codomain using only its cited source.

This diagnostic intentionally does NOT change canonical backward-search selection.
It establishes whether source-scoped resolution is a viable distinct dependency.
"""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import TodaHopfInvariantMap, TodaPrimaryGroup
from phase165_r3_recursive_search import (
    RegisteredGoalUnresolved, reconstruct_registered_goal,
)
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates, search_group_from_registered_goal,
)
from phase165_r57_r8_eta_specialization import (
    _is_generic_eta_group_relation, expand_registered_eta_specialization,
    specialize_eta_group_relation,
)
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import ProofRule
from toda_rules import TodaHopfInvariantSurjectiveStatement

PACKAGE = Path(__file__).resolve().parent


def examine() -> dict:
    bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=3, k=2)
    if len(candidates) != 1:
        raise AssertionError('Expected one registered pi5^3 target')
    target = candidates[0]
    citing_id = resolve_specialized_goal_citing_id(bridge, target)
    if not citing_id:
        raise AssertionError('Missing goal citation binding')
    contexts = []
    complete = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=contexts.append,
    )
    if complete.status is not ProofSearchStatus.COMPLETE or len(contexts) != 1:
        raise AssertionError('Completed pi5^3 baseline was not found')
    screened = contexts[0]
    hopf_goal = TodaHopfInvariantSurjectiveStatement(
        TodaHopfInvariantMap(
            TodaPrimaryGroup(6, 3), TodaPrimaryGroup(6, 5),
        )
    )
    codomain_group = hopf_goal.map.target_group
    source_links = tuple(
        link for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and _is_generic_eta_group_relation(link.step.conclusion)
        and precedes_citing_assertion(screened, link.assertion_id, citing_id)
    )
    if len(source_links) != 1:
        raise AssertionError('Expected one screened prior higher-eta source')
    source_link = source_links[0]
    schema = source_link.step.conclusion
    specific = specialize_eta_group_relation(schema, codomain_group.sphere_dimension)
    if specific.lhs != codomain_group:
        raise AssertionError('Source specialization does not match the Hopf codomain')

    # A source-bound provider is a *read-only experiment*, not a replacement
    # for the public shared provider or an automatic priority preference.
    def source_bound(goal):
        return expand_registered_eta_specialization(goal, (schema,))

    proposals = source_bound(specific)
    if len(proposals) != 1 or proposals[0].subgoals != (schema,):
        raise AssertionError('Cited direct specialization is not unique')
    proof = reconstruct_registered_goal(
        specific, screened, citing_id, source_bound,
        lookup_mode='typed_reference_publication',
    )
    if not (proof.rule is ProofRule.INFERENCE
            and proof.conclusion == specific
            and len(proof.premises) == 1
            and proof.premises[0] is source_link.step):
        raise AssertionError('Source-bound proof failed its exact given ancestry')

    def empty_source_provider(goal):
        return expand_registered_eta_specialization(goal, ())

    missing_source_failed_closed = False
    try:
        reconstruct_registered_goal(
            specific, screened, citing_id, empty_source_provider,
            lookup_mode='typed_reference_publication',
        )
    except RegisteredGoalUnresolved:
        missing_source_failed_closed = True

    # In the unchanged public provider, the two independent historical routes
    # remain discoverable. Never suppress the transport proof in this audit.
    shared = shared_expansion_provider(screened, proof_target=target)
    public_routes = tuple(
        getattr(option.rule, 'name', '<unnamed>') for option in shared(specific)
    )
    literature = getattr(source_link.step.inference_rule, 'literature_reference', None)
    return {
        'phase': '169-R3X',
        'mode': 'AUDIT_ONLY',
        'pi53_status': complete.status.value,
        'source_assertion_id': source_link.assertion_id,
        'source_locator': getattr(literature, 'locator', None),
        'source_prior_to_goal': True,
        'bound_goal': repr(specific),
        'source_bound_proposal_count': len(proposals),
        'bound_proof_rule': proof.rule.value,
        'bound_proof_inference': getattr(proof.inference_rule, 'name', None),
        'bound_proof_premise_rule': proof.premises[0].rule.value,
        'bound_proof_citation_id': source_link.assertion_id,
        'missing_source_failed_closed': missing_source_failed_closed,
        'public_provider_route_names': list(public_routes),
        'public_provider_unchanged': True,
        'production_modified': False,
        'existing_tests_modified': False,
        'full_pytest_run': False,
    }


def main() -> None:
    report = examine()
    output = PACKAGE / 'output' / 'r3x_source_bound_eta_probe.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    for key in ('pi53_status', 'source_assertion_id', 'source_locator',
                'source_bound_proposal_count', 'bound_proof_rule',
                'bound_proof_inference', 'bound_proof_premise_rule',
                'missing_source_failed_closed', 'public_provider_route_names'):
        print('R3X_' + key.upper() + '=' + repr(report[key]))
    print('R3X_AUDIT_ONLY=True')
    print('R3X_FULL_PYTEST_RUN=False')
    print('R3X_REPORT=' + str(output))


if __name__ == '__main__':
    main()

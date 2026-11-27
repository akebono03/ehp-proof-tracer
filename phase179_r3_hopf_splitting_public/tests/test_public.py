"""Public candidate and certified-premise replay, without altering source registry."""
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase174_r3_r6_r2_prop44_lemma54.source import expand_cited_preprop44_splitting
from phase178_r19_finite_cyclic_suspension_transport_isolated.provider import suspension_transport_inputs
from phase179_r2_hopf_splitting_injectivity_isolated.rule import (
    RULE_NAME, SOURCE, expand_splitting_injectivity, screened_splitting_steps,
)
from proof import ProofRule, apply_inference_match, find_inference_matches_for_rule


def test_boundary_public_provider_replays_cited_injectivity():
    root = exact_prior_database_result(8, 6)
    lower = exact_prior_database_result(7, 6)
    assert root is not None and lower is not None
    required = suspension_transport_inputs(root, lower)
    assert required is not None
    goal = MapInjective(required[1].map)
    bridge = prefer_universal_prop42_derivation(
        screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    )
    snapshot = tuple(bridge.proof_links), tuple(bridge.registry._assertions.items())
    provider = shared_expansion_provider(bridge, proof_target=root)
    assert any(option.subgoals == required for option in provider(root))
    isolated, = expand_splitting_injectivity(goal, bridge=bridge)
    public, = tuple(option for option in provider(goal) if option.rule.name == RULE_NAME)
    assert public.subgoals == isolated.subgoals == (SOURCE,)
    source, = screened_splitting_steps(bridge)
    match, = find_inference_matches_for_rule(public.rule, (source,))
    step = apply_inference_match(match)
    assert step.rule is ProofRule.INFERENCE and step.conclusion == goal
    assert step.premises == (source,)
    assert tuple(bridge.proof_links) == snapshot[0]
    assert tuple(bridge.registry._assertions.items()) == snapshot[1]
    print('PHASE179_R3_BOUNDARY_PUBLIC_INJECTIVITY=VERIFIED')


def test_public_does_not_duplicate_legacy_hopf_four_or_extend_unlisted_dimensions():
    root = exact_prior_database_result(8, 6)
    assert root is not None
    bridge = prefer_universal_prop42_derivation(
        screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    )
    provider = shared_expansion_provider(bridge, proof_target=root)
    available = tuple(link.step.conclusion for link in bridge.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    goal4 = MapInjective(TodaSuspensionMap(TodaPrimaryGroup(5, 3), TodaPrimaryGroup(6, 4)))
    legacy = expand_cited_preprop44_splitting(goal4, available)
    actual = tuple(option for option in provider(goal4) if option.rule.name == RULE_NAME)
    assert len(actual) == len(legacy)
    assert tuple(option.subgoals for option in actual) == tuple(option.subgoals for option in legacy)
    goal9 = MapInjective(TodaSuspensionMap(TodaPrimaryGroup(15, 8), TodaPrimaryGroup(16, 9)))
    assert not any(option.rule.name == RULE_NAME for option in provider(goal9))

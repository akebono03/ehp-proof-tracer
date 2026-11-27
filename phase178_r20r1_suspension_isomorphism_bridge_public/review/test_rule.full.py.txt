"""Conditional matcher tests and real source-screened isolated proposals."""
from dataclasses import replace

import pytest

from homotopy_groups import (
    TodaDeltaMap, TodaPrimaryGroup, TodaSuspensionIsomorphismStatement, TodaSuspensionMap,
)
from phase165_r14_r6_generic_iso import (
    MapInjective, MapSurjective, MapIsomorphism, expand_generic_iso_goal,
)
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase178_r19_finite_cyclic_suspension_transport_isolated.provider import suspension_transport_inputs
from phase178_r20_suspension_isomorphism_bridge_isolated.rule import (
    RULE_NAME, suspension_isomorphism_inputs, suspension_isomorphism_bridge_rule,
    expand_suspension_isomorphism_bridge,
)
from proof import ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule


def mapping(n, k):
    return TodaSuspensionMap(TodaPrimaryGroup(n+k,n), TodaPrimaryGroup(n+k+1,n+1))


def infer_generic_iso(e):
    # Synthetic hypotheses for conditional replay ONLY, not actual literature or registry leaves.
    option, = expand_generic_iso_goal(MapIsomorphism(e))
    parents = tuple(ProofStep(g,(),ProofRule.GIVEN) for g in option.subgoals)
    match, = find_inference_matches_for_rule(option.rule, parents)
    return apply_inference_match(match)


@pytest.mark.parametrize('n,k', [(2,0),(3,2),(5,6),(6,6),(10,9)])
def test_general_bridge_reuses_existing_iso(n,k):
    e = mapping(n,k)
    goal = TodaSuspensionIsomorphismStatement(e)
    option, = expand_suspension_isomorphism_bridge(goal)
    assert option.rule.name == RULE_NAME and option.rule.literature_reference is None
    assert option.subgoals == (MapIsomorphism(e),)
    generic, = expand_generic_iso_goal(option.subgoals[0])
    assert generic.subgoals == (MapInjective(e),MapSurjective(e))
    iso = infer_generic_iso(e)
    match, = find_inference_matches_for_rule(option.rule,(iso,))
    result = apply_inference_match(match)
    assert result.rule is ProofRule.INFERENCE and result.conclusion == goal
    assert result.premises == (iso,)
    assert tuple(p.conclusion for p in iso.premises) == generic.subgoals
    for p in iso.premises:
        assert not find_inference_matches_for_rule(option.rule,(p,))
        assert not find_inference_matches_for_rule(generic.rule,(p,))


@pytest.mark.parametrize('goal', [
    MapIsomorphism(mapping(5,6)), MapInjective(mapping(5,6)),
    TodaSuspensionIsomorphismStatement(TodaDeltaMap(TodaPrimaryGroup(13,11),TodaPrimaryGroup(11,5))),
    TodaSuspensionIsomorphismStatement(TodaSuspensionMap(TodaPrimaryGroup(11,5),TodaPrimaryGroup(13,6))),
    TodaSuspensionIsomorphismStatement(TodaSuspensionMap(TodaPrimaryGroup(11,5),TodaPrimaryGroup(12,7))),
    TodaSuspensionIsomorphismStatement(mapping(1,2)),
    TodaSuspensionIsomorphismStatement(mapping(5,-1)),
    TodaSuspensionIsomorphismStatement(TodaSuspensionMap(TodaPrimaryGroup(5,True),TodaPrimaryGroup(6,2))),
    TodaSuspensionIsomorphismStatement(TodaSuspensionMap(TodaPrimaryGroup(2,2),TodaPrimaryGroup(3.0,3))),
    TodaSuspensionIsomorphismStatement(TodaSuspensionMap('a','b')),
])
def test_invalid_goals_fail_closed(goal):
    assert suspension_isomorphism_inputs(goal) is None
    assert expand_suspension_isomorphism_bridge(goal) == ()
    with pytest.raises(ValueError):
        suspension_isomorphism_bridge_rule(goal)


def test_reject_mismatched_and_unproved_map_property():
    e = mapping(5,6)
    rule = suspension_isomorphism_bridge_rule(TodaSuspensionIsomorphismStatement(e))
    iso = infer_generic_iso(e)
    assert not find_inference_matches_for_rule(rule,())
    assert not find_inference_matches_for_rule(rule,(infer_generic_iso(mapping(6,6)),))
    assert not find_inference_matches_for_rule(rule,(replace(iso,rule=ProofRule.GIVEN),))
    assert not find_inference_matches_for_rule(rule,(replace(iso,premises=()),))
    assert not find_inference_matches_for_rule(rule,(replace(iso,inference_rule=None),))


def test_real_n6_frontier_and_existing_obligations():
    root = exact_prior_database_result(6,6)
    lower = exact_prior_database_result(5,6)
    assert root is not None and lower is not None
    required = suspension_transport_inputs(root,lower)
    assert required is not None
    bridge = prefer_universal_prop42_derivation(screen_independent_sources_for_derived_goal(build_shared_typed_bridge(),goal=root))
    links, assertions = tuple(bridge.proof_links), tuple(bridge.registry._assertions.items())
    public = shared_expansion_provider(bridge,proof_target=root)
    assert any(o.subgoals == required for o in public(root))
    goal = required[1]
    assert sum(o.rule.name == RULE_NAME and o.subgoals == (MapIsomorphism(goal.map),)
               for o in public(goal)) == 1
    proposal, = expand_suspension_isomorphism_bridge(goal)
    generic, = proposal.subgoals
    assert isinstance(generic,MapIsomorphism)
    injective, surjective = MapInjective(goal.map), MapSurjective(goal.map)
    assert any(o.rule.name == 'generic injective and surjective imply isomorphism'
               and o.subgoals == (injective,surjective) for o in public(generic))
    assert any(o.rule.name == 'EHP zero Delta and Delta-E exactness imply suspension injectivity' for o in public(injective))
    assert any(o.rule.name == 'injective Delta and consecutive EHP exactness imply suspension surjectivity' for o in public(surjective))
    assert not any(isinstance(x,ProofStep) for x in proposal.subgoals)
    assert tuple(bridge.proof_links) == links
    assert tuple(bridge.registry._assertions.items()) == assertions
    print('PHASE178_R20_N6_TYPED_ISOMORPHISM_BRIDGE=VERIFIED')
    print('PHASE178_R20_EXISTING_INJECTIVE_SURJECTIVE_CANDIDATES=VERIFIED')
    print('PHASE178_R20R1_PUBLIC_PROVIDER_MATCH=VERIFIED')
    for g in (goal,generic,injective,surjective):
        print('PHASE178_R20_OBLIGATION='+repr(g))

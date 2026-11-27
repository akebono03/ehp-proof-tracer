from dataclasses import replace

import pytest

from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase174_r3_r6_r2_prop44_lemma54.source import (
    build_cited_preprop44_splitting, expand_cited_preprop44_splitting, verify_prelude_source,
)
from phase178_r19_finite_cyclic_suspension_transport_isolated.provider import suspension_transport_inputs
from phase179_r2_hopf_splitting_injectivity_isolated.rule import (
    SOURCE, RULE_NAME, splitting_inputs, screened_splitting_steps,
    splitting_injectivity_rule, expand_splitting_injectivity,
)
from proof import ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule


def goal(n, q):
    return MapInjective(TodaSuspensionMap(TodaPrimaryGroup(q, n-1), TodaPrimaryGroup(q+1, n)))


@pytest.mark.parametrize('n,q', [(2,2),(2,5),(4,3),(4,9),(8,7),(8,13),(8,14),(8,20)])
def test_cited_split_injection_general(n,q):
    bridge = build_cited_preprop44_splitting()
    target = goal(n,q)
    assert splitting_inputs(target) == (SOURCE,)
    step, = screened_splitting_steps(bridge)
    option, = expand_splitting_injectivity(target,bridge=bridge)
    assert option.subgoals == (SOURCE,)
    match, = find_inference_matches_for_rule(option.rule,(step,))
    result = apply_inference_match(match)
    assert result.rule is ProofRule.INFERENCE
    assert result.conclusion == target and result.premises == (step,)
    assert option.rule.name == RULE_NAME


@pytest.mark.parametrize('target', [goal(3,5),goal(5,7),goal(7,13),goal(9,15),goal(8,5),
    MapSurjective(goal(8,13).map),
    MapInjective(TodaSuspensionMap(TodaPrimaryGroup(13,7),TodaPrimaryGroup(15,8))),
    MapInjective(TodaSuspensionMap(TodaPrimaryGroup(13,7),TodaPrimaryGroup(14,9))),
    MapInjective(TodaSuspensionMap(TodaPrimaryGroup(13,7),TodaPrimaryGroup(14.0,8))),
    MapInjective(TodaDeltaMap(TodaPrimaryGroup(15,15),TodaPrimaryGroup(13,7))),
    MapInjective(TodaSuspensionMap('a','b'))])
def test_wrong_map_or_dimensions_rejected(target):
    bridge = build_cited_preprop44_splitting()
    assert splitting_inputs(target) is None
    assert expand_splitting_injectivity(target,bridge=bridge) == ()
    with pytest.raises(ValueError):
        splitting_injectivity_rule(target,bridge=bridge)


def test_missing_duplicate_and_unlinked_hypotheses_rejected():
    bridge = build_cited_preprop44_splitting()
    target = goal(8,13)
    assert not expand_splitting_injectivity(target,bridge=replace(bridge,proof_links=()))
    assert not expand_splitting_injectivity(target,bridge=replace(bridge,proof_links=bridge.proof_links*2))
    rule = splitting_injectivity_rule(target,bridge=bridge)
    step, = screened_splitting_steps(bridge)
    for wrong in (ProofStep(SOURCE,(),ProofRule.GIVEN),
                  replace(step,rule=ProofRule.INFERENCE),
                  replace(step,conclusion=replace(SOURCE,dimensions=(2,4))),
                  replace(step,premises=(step,))):
        assert not find_inference_matches_for_rule(rule,(wrong,))
    assert not find_inference_matches_for_rule(rule,())


def test_real_boundary_source_and_unconnected_public_provider():
    assert verify_prelude_source() == 7250
    root = exact_prior_database_result(8,6)
    lower = exact_prior_database_result(7,6)
    assert root is not None and lower is not None
    required = suspension_transport_inputs(root,lower)
    assert required is not None
    target = MapInjective(required[1].map)
    assert target == goal(8,13)
    bridge = prefer_universal_prop42_derivation(screen_independent_sources_for_derived_goal(build_shared_typed_bridge(),goal=root))
    links, assertions = tuple(bridge.proof_links), tuple(bridge.registry._assertions.items())
    source, = screened_splitting_steps(bridge)
    available = tuple(link.step.conclusion for link in links if link.step is not None and link.step.rule is ProofRule.GIVEN)
    assert expand_cited_preprop44_splitting(target,available) == ()
    public = shared_expansion_provider(bridge,proof_target=root)
    assert any(o.subgoals == required for o in public(root))
    assert not any(o.rule.name == RULE_NAME for o in public(target))
    option, = expand_splitting_injectivity(target,bridge=bridge)
    match, = find_inference_matches_for_rule(option.rule,(source,))
    step = apply_inference_match(match)
    assert step.conclusion == target and step.premises == (source,)
    assert step.rule is ProofRule.INFERENCE
    assert tuple(bridge.proof_links) == links and tuple(bridge.registry._assertions.items()) == assertions
    print('PHASE179_R2_BOUNDARY_INJECTIVITY_ISOLATED=VERIFIED')
    print('PHASE179_R2_PUBLIC_PROVIDER_CHANGED=NO')

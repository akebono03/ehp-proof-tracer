"""Generic EHP H-zero proof obligations and negative guards."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import (
    TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup, TodaSuspensionMap,
)
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase175_r4r12r13r4_hopf_zero_public import installer, provider
from phase175_r4r12r13r4_hopf_zero_public.rule import (
    DELTA_TO_H_ZERO, H_ZERO_TO_E_SURJ,
    expand_hopf_zero_from_injective_delta,
    expand_suspension_surjective_from_zero_hopf,
    hopf_zero_inputs, suspension_surjective_inputs,
)
from proof import InferenceRule, ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule
from toda_rules import TodaHopfInvariantZeroStatement


def e_goal() -> MapSurjective:
    return MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(8, 4), TodaPrimaryGroup(9, 5)))


def invented_proof(statement: object, rule: ProofRule = ProofRule.INFERENCE) -> ProofStep:
    return ProofStep(statement, (), rule, inference_rule=InferenceRule("test-only"))


def test_hopf_zero_is_intermediate_goal_not_zero_codomain() -> None:
    e_required = suspension_surjective_inputs(e_goal())
    assert e_required is not None
    h_goal, e_h = e_required
    assert isinstance(h_goal, TodaHopfInvariantZeroStatement)
    assert h_goal.map == TodaHopfInvariantMap(TodaPrimaryGroup(9, 5), TodaPrimaryGroup(9, 9))
    h_required = hopf_zero_inputs(h_goal)
    assert h_required is not None
    delta, h_delta = h_required
    assert delta == MapInjective(TodaDeltaMap(TodaPrimaryGroup(9, 9), TodaPrimaryGroup(7, 4)))
    assert e_h.window.target_term == h_delta.window.middle_term


def test_two_backward_expansions_are_visible() -> None:
    h_goal = suspension_surjective_inputs(e_goal())[0]
    assert len(provider.expand_public_hopf_zero_ehp(e_goal())) == 1
    assert len(provider.expand_public_hopf_zero_ehp(h_goal)) == 1
    assert provider.expand_public_hopf_zero_ehp(MapInjective(h_goal.map)) == ()


def test_zero_hopf_rule_accepts_only_both_proven_parents() -> None:
    h_goal = suspension_surjective_inputs(e_goal())[0]
    expansion = expand_hopf_zero_from_injective_delta(h_goal)[0]
    assert expansion.rule.name == DELTA_TO_H_ZERO
    parents = tuple(invented_proof(x) for x in expansion.subgoals)
    matches = find_inference_matches_for_rule(expansion.rule, parents)
    assert len(matches) == 1
    assert apply_inference_match(matches[0]).conclusion == h_goal
    assert not find_inference_matches_for_rule(expansion.rule, parents[:1])
    assert not find_inference_matches_for_rule(
        expansion.rule, (invented_proof(parents[0].conclusion, ProofRule.GIVEN), parents[1]),
    )


def test_surjectivity_rule_accepts_only_zero_map_and_exactness() -> None:
    expansion = expand_suspension_surjective_from_zero_hopf(e_goal())[0]
    assert expansion.rule.name == H_ZERO_TO_E_SURJ
    parents = tuple(invented_proof(x) for x in expansion.subgoals)
    matches = find_inference_matches_for_rule(expansion.rule, parents)
    assert len(matches) == 1
    assert apply_inference_match(matches[0]).conclusion == e_goal()
    assert not find_inference_matches_for_rule(expansion.rule, parents[:1])


def test_wrong_hopf_map_dimensions_are_rejected() -> None:
    normal = suspension_surjective_inputs(e_goal())[0]
    wrong = TodaHopfInvariantZeroStatement(TodaHopfInvariantMap(
        TodaPrimaryGroup(9, 5), TodaPrimaryGroup(9, 8)))
    assert hopf_zero_inputs(wrong) is None
    assert expand_hopf_zero_from_injective_delta(wrong) == ()
    assert hopf_zero_inputs(normal) is not None


def test_invalid_e_map_dimensions_rejected() -> None:
    wrong = MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(8, 4), TodaPrimaryGroup(9, 6)))
    assert suspension_surjective_inputs(wrong) is None
    assert expand_suspension_surjective_from_zero_hopf(wrong) == ()


def test_installer_idempotence_and_fail_closed_anchor() -> None:
    source = "def shared_expansion_provider(bridge):\n" + installer.ANCHOR + "    return ()\n"
    changed, required = installer.render(source)
    assert required and changed.count("expand_public_hopf_zero_ehp") == 2
    assert installer.render(changed) == (changed, False)
    with pytest.raises(RuntimeError, match="ANCHOR"):
        installer.render("def not_the_public_provider():\n    return ()\n")

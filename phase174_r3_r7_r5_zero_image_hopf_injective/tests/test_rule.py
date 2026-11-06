"""Focused tests of the generic, isolated EHP zero-image inference."""
from __future__ import annotations

import pytest

from homotopy_groups import (
    TodaEHPExactnessWindow, TodaHopfInvariantMap, TodaPrimaryGroup,
    TodaPrimaryGroupZeroStatement, TodaSuspensionMap,
)
from map_facts import EHP_E_MAP, EHP_H_MAP
from map_property_rules import ImageZeroStatement
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapInjective
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
    RULE_NAME, expand_hopf_injective_from_zero_image,
    hopf_injectivity_from_zero_image_inputs,
    hopf_injective_from_zero_image_rule,
)
from proof import InferenceRule, ProofRule, ProofStep, find_inference_matches_for_rule
from toda_rules import TodaProp42ExactnessStatement


def _goal(q: int, sphere: int) -> MapInjective:
    return MapInjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(q, sphere),
        TodaPrimaryGroup(q, 2 * sphere - 1),
    ))


def _hypothetical(statement: object) -> ProofStep:
    """A fixture only: no source claim or verified proof is created."""
    return ProofStep(
        conclusion=statement, premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="hypothetical-test-fixture"),
    )


def test_pi116_hopf_goal_has_zero_image_not_zero_group_subgoal() -> None:
    goal = _goal(11, 6)
    requirements = hopf_injectivity_from_zero_image_inputs(goal)
    assert requirements is not None
    image, exactness = requirements
    assert image == ImageZeroStatement(TodaSuspensionMap(
        TodaPrimaryGroup(10, 5), TodaPrimaryGroup(11, 6),
    ))
    assert exactness == TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        TodaPrimaryGroup(10, 5), TodaPrimaryGroup(11, 6),
        TodaPrimaryGroup(11, 11), EHP_E_MAP, EHP_H_MAP,
    ))
    assert prop42_exactness_indices(exactness) == (5, 11, "e_h")
    assert all(not isinstance(x, TodaPrimaryGroupZeroStatement) for x in requirements)


@pytest.mark.parametrize("q,sphere", ((3, 2), (7, 4), (11, 6), (15, 8)))
def test_rule_is_dimension_generic(q: int, sphere: int) -> None:
    goal = _goal(q, sphere)
    options = expand_hopf_injective_from_zero_image(goal)
    assert len(options) == 1
    assert options[0].rule.name == RULE_NAME
    assert options[0].subgoals == hopf_injectivity_from_zero_image_inputs(goal)
    assert prop42_exactness_indices(options[0].subgoals[1]) == (
        sphere - 1, q, "e_h",
    )


@pytest.mark.parametrize("bad", (
    object(), "injective", MapInjective(object()),
    MapInjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(11, 6), TodaPrimaryGroup(11, 10),
    )),
    MapInjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(4, 6), TodaPrimaryGroup(4, 11),
    )),
    MapInjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(11, "6"), TodaPrimaryGroup(11, 11),
    )),
))
def test_invalid_or_mismatched_hopf_goals_rejected(bad: object) -> None:
    assert hopf_injectivity_from_zero_image_inputs(bad) is None
    assert expand_hopf_injective_from_zero_image(bad) == ()


def test_hypothetical_inference_premises_match_without_proof_claim() -> None:
    goal = _goal(11, 6)
    required = hopf_injectivity_from_zero_image_inputs(goal)
    assert required is not None
    steps = tuple(_hypothetical(x) for x in required)
    rule = hopf_injective_from_zero_image_rule(goal)
    matches = find_inference_matches_for_rule(rule, steps)
    assert len(matches) == 1
    derived = derive_inference_proof_step(matches[0])
    assert derived.conclusion == goal
    assert derived.rule is ProofRule.INFERENCE
    assert derived.premises == steps
    assert derived.inference_rule is rule


def test_direct_given_cannot_discharge_zero_image_or_exactness() -> None:
    goal = _goal(11, 6)
    required = hopf_injectivity_from_zero_image_inputs(goal)
    assert required is not None
    rule = hopf_injective_from_zero_image_rule(goal)
    steps = tuple(_hypothetical(x) for x in required)
    for index in (0, 1):
        forbidden = list(steps)
        forbidden[index] = ProofStep(required[index], (), ProofRule.GIVEN)
        assert find_inference_matches_for_rule(rule, tuple(forbidden)) == ()


def test_mixed_map_or_reversed_premises_rejected() -> None:
    goal = _goal(11, 6)
    required = hopf_injectivity_from_zero_image_inputs(goal)
    other = hopf_injectivity_from_zero_image_inputs(_goal(9, 5))
    assert required is not None and other is not None
    rule = hopf_injective_from_zero_image_rule(goal)
    assert find_inference_matches_for_rule(rule, (
        _hypothetical(other[0]), _hypothetical(required[1]),
    )) == ()
    assert find_inference_matches_for_rule(rule, (
        _hypothetical(required[0]), _hypothetical(other[1]),
    )) == ()
    assert rule.match_guard(tuple(_hypothetical(x) for x in reversed(required)), {}) is False


def test_expansion_never_creates_proofsteps_or_target_given() -> None:
    goal = _goal(11, 6)
    options = expand_hopf_injective_from_zero_image(goal)
    assert len(options) == 1
    assert all(not isinstance(x, ProofStep) for x in options[0].subgoals)
    assert goal not in options[0].subgoals

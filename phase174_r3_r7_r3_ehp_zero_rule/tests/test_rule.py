"""Focused contract checks for the generic EHP zero inference."""
from __future__ import annotations

import pytest

from homotopy_groups import (
    TodaDeltaMap, TodaEHPExactnessWindow, TodaPrimaryGroup,
    TodaPrimaryGroupZeroStatement,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapSurjective
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase174_r3_r7_r3_ehp_zero_rule.rule import (
    RULE_NAME,
    ehp_zero_from_delta_surjectivity_rule,
    ehp_zero_inputs,
    expand_ehp_zero_from_delta_surjectivity,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, find_inference_matches_for_rule,
)
from toda_rules import TodaProp42ExactnessStatement


def _goal(i: int, sphere: int) -> TodaPrimaryGroupZeroStatement:
    return TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(i, sphere))


def _inferred(statement: object) -> ProofStep:
    """Only a fixture; a real proof tree must verify every such subgoal."""
    return ProofStep(
        conclusion=statement, premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only hypothetical premise"),
    )


def test_pi127_exactly_four_typed_premises() -> None:
    root = _goal(12, 7)
    required = ehp_zero_inputs(root)
    assert required is not None
    surjective, de, eh, terminal = required
    assert surjective == MapSurjective(TodaDeltaMap(
        TodaPrimaryGroup(13, 13), TodaPrimaryGroup(11, 6)
    ))
    assert prop42_exactness_indices(de) == (6, 12, "delta_e")
    assert prop42_exactness_indices(eh) == (6, 12, "e_h")
    assert terminal == _goal(12, 13)
    options = expand_ehp_zero_from_delta_surjectivity(root)
    assert len(options) == 1
    assert options[0].subgoals == required
    assert options[0].rule.name == RULE_NAME


@pytest.mark.parametrize("group_dimension,sphere_dimension", (
    (9, 5), (10, 6), (12, 7), (14, 8),
))
def test_generic_no_stem_enumeration(
    group_dimension: int, sphere_dimension: int,
) -> None:
    root = _goal(group_dimension, sphere_dimension)
    goals = ehp_zero_inputs(root)
    assert goals is not None
    n = sphere_dimension - 1
    assert prop42_exactness_indices(goals[1]) == (n, group_dimension, "delta_e")
    assert prop42_exactness_indices(goals[2]) == (n, group_dimension, "e_h")
    assert goals[3] == _goal(group_dimension, 2 * n + 1)


@pytest.mark.parametrize("candidate", (
    object(), "zero", _goal(3, 5), _goal(1, 1),
    TodaPrimaryGroupZeroStatement(TodaPrimaryGroup("12", 7)),
    TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, "7")),
))
def test_invalid_target_has_no_backward_candidate(candidate: object) -> None:
    assert ehp_zero_inputs(candidate) is None
    assert expand_ehp_zero_from_delta_surjectivity(candidate) == ()


def test_valid_premises_derive_only_through_inference_match() -> None:
    target = _goal(12, 7)
    goals = ehp_zero_inputs(target)
    assert goals is not None
    rule = ehp_zero_from_delta_surjectivity_rule(target)
    proofs = tuple(_inferred(statement) for statement in goals)
    matches = find_inference_matches_for_rule(rule, proofs)
    assert len(matches) == 1
    result = derive_inference_proof_step(matches[0])
    assert result.conclusion == target
    assert result.rule is ProofRule.INFERENCE
    assert result.premises == proofs
    assert result.inference_rule is rule


def test_direct_given_cannot_replace_independently_inferred_premise() -> None:
    target = _goal(12, 7)
    goals = ehp_zero_inputs(target)
    assert goals is not None
    rule = ehp_zero_from_delta_surjectivity_rule(target)
    proofs = list(_inferred(statement) for statement in goals)
    for index in range(4):
        tampered = list(proofs)
        tampered[index] = ProofStep(goals[index], (), ProofRule.GIVEN)
        assert find_inference_matches_for_rule(rule, tuple(tampered)) == ()


def test_wrong_delta_map_and_wrong_terminal_are_rejected() -> None:
    target = _goal(12, 7)
    goals = ehp_zero_inputs(target)
    assert goals is not None
    rule = ehp_zero_from_delta_surjectivity_rule(target)
    proofs = tuple(_inferred(statement) for statement in goals)
    bad_delta = _inferred(MapSurjective(TodaDeltaMap(
        TodaPrimaryGroup(15, 15), TodaPrimaryGroup(13, 7)
    )))
    bad_terminal = _inferred(_goal(13, 13))
    assert find_inference_matches_for_rule(rule, (bad_delta,) + proofs[1:]) == ()
    assert find_inference_matches_for_rule(rule, proofs[:3] + (bad_terminal,)) == ()


def test_windows_must_be_consecutive_and_in_correct_order() -> None:
    target = _goal(12, 7)
    goals = ehp_zero_inputs(target)
    assert goals is not None
    rule = ehp_zero_from_delta_surjectivity_rule(target)
    proofs = tuple(_inferred(statement) for statement in goals)
    # The matcher is permutation-insensitive; the ordered proof contract is
    # nevertheless strict for actual reconstructed parent slots.
    assert rule.match_guard((proofs[0], proofs[2], proofs[1], proofs[3]), {}) is False
    bad_window = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(13, 13),
        middle_term=TodaPrimaryGroup(11, 6),
        target_term=TodaPrimaryGroup(12, 7),
        first_map=EHP_E_MAP,
        second_map=EHP_DELTA_MAP,
    ))
    assert find_inference_matches_for_rule(rule, (
        proofs[0], _inferred(bad_window), proofs[2], proofs[3],
    )) == ()


def test_no_target_group_given_is_constructed() -> None:
    root = _goal(12, 7)
    options = expand_ehp_zero_from_delta_surjectivity(root)
    assert len(options) == 1
    assert all(type(goal) is not ProofStep for goal in options[0].subgoals)
    assert root not in options[0].subgoals

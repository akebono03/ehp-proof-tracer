"""Focused tests for the generic Delta-zero bridge (not public certification)."""
from __future__ import annotations

from homotopy_groups import (
    TodaDeltaMap,
    TodaEHPExactnessWindow,
    TodaPrimaryGroup,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase174_r3_r3_injective_delta_zero.rule import (
    delta_e_injectivity_inputs,
    delta_zero_from_injection_rule,
    expand_delta_zero_from_injection,
)
from proof import ProofRule, ProofStep, find_inference_matches_for_rule
from toda_rules import TodaDeltaZeroStatement, TodaProp42ExactnessStatement


def goal_for(q: int, n: int) -> TodaDeltaZeroStatement:
    return TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(q + 2, 2 * n + 1),
        TodaPrimaryGroup(q, n),
    ))


def test_expected_pi85_delta_subgoals_are_well_typed() -> None:
    goal = goal_for(5, 3)
    injection, exactness = delta_e_injectivity_inputs(goal)
    assert injection.map.source_group == TodaPrimaryGroup(5, 3)
    assert injection.map.target_group == TodaPrimaryGroup(6, 4)
    assert exactness.window.source_term == TodaPrimaryGroup(7, 7)
    assert exactness.window.first_map == EHP_DELTA_MAP
    assert exactness.window.second_map == EHP_E_MAP


def test_generic_rule_accepts_matching_inferred_contract_steps() -> None:
    goal = goal_for(5, 3)
    expansion = expand_delta_zero_from_injection(goal)[0]
    # Synthetic inferred steps exercise matching only; they do not establish
    # independent citation provenance, which the live audit checks.
    inputs = tuple(ProofStep(x, (), ProofRule.INFERENCE) for x in expansion.subgoals)
    matches = find_inference_matches_for_rule(expansion.rule, inputs)
    assert len(matches) == 1
    proof = derive_inference_proof_step(matches[0])
    assert proof.rule is ProofRule.INFERENCE
    assert proof.conclusion == goal
    assert proof.premises == inputs


def test_does_not_accept_direct_given_as_valid_injection() -> None:
    expansion = expand_delta_zero_from_injection(goal_for(5, 3))[0]
    injection, exactness = expansion.subgoals
    inputs = (
        ProofStep(injection, (), ProofRule.GIVEN),
        ProofStep(exactness, (), ProofRule.INFERENCE),
    )
    assert find_inference_matches_for_rule(expansion.rule, inputs) == ()


def test_wrong_suspension_map_is_rejected() -> None:
    goal = goal_for(5, 3)
    expansion = expand_delta_zero_from_injection(goal)[0]
    injection, exactness = expansion.subgoals
    other = delta_e_injectivity_inputs(goal_for(7, 4))[0]
    steps = (
        ProofStep(other, (), ProofRule.INFERENCE),
        ProofStep(exactness, (), ProofRule.INFERENCE),
    )
    assert find_inference_matches_for_rule(expansion.rule, steps) == ()


def test_wrong_exactness_window_is_rejected() -> None:
    goal = goal_for(5, 3)
    expansion = expand_delta_zero_from_injection(goal)[0]
    injection, exactness = expansion.subgoals
    w = exactness.window
    wrong = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        w.source_term, w.middle_term, w.target_term, EHP_E_MAP, EHP_DELTA_MAP,
    ))
    steps = (
        ProofStep(injection, (), ProofRule.INFERENCE),
        ProofStep(wrong, (), ProofRule.INFERENCE),
    )
    assert find_inference_matches_for_rule(expansion.rule, steps) == ()


def test_general_dimension_and_fail_closed_outside_valid_range() -> None:
    assert len(expand_delta_zero_from_injection(goal_for(7, 4))) == 1
    assert expand_delta_zero_from_injection(goal_for(5, 4)) == ()
    assert expand_delta_zero_from_injection("Delta zero") == ()


def test_result_not_certified_from_rule_registration_alone() -> None:
    from phase174_r3_r3_injective_delta_zero.audit import validate_prior_r3r2
    report = {
        "phase": "174-R3-R2",
        "mode": "READ_ONLY_CYCLIC_EXTENSION_GAP",
        "local_head": "8687759569d7820e26c53aac6f38aedb8ea04f0b",
        "cyclic_children_count": 2,
        "cyclic_children_no_second_hop": True,
        "cyclic_children_exact_target_match": [True, True],
        "new_given": 0,
        "new_proof_steps": 0,
        "full_pytest_performed": False,
        "extension_obligations": {"requirements": [{}] * 5},
    }
    assert validate_prior_r3r2(report)["new_proof_steps"] == 0
    report["new_given"] = 1
    try:
        validate_prior_r3r2(report)
    except ValueError:
        pass
    else:
        raise AssertionError("the previous audit's proof boundary was ignored")

"""Focused terminal-goal proposals; these tests do not certify source claims."""
from __future__ import annotations

import pytest

from homotopy_groups import (
    TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup,
)
from phase165_r14_r5_ehp_connection import expand_registered_ehp_terminal_goal
from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
from proof import ProofRule, ProofStep, find_inference_matches_for_rule, apply_inference_match
from toda_rules import (
    TodaDeltaInjectiveStatement, TodaHopfInvariantSurjectiveStatement,
    TodaProp51FiniteDimensionalStatement,
)


def _source():
    bridge = build_adopted_prop51_reference()
    claim = bridge.registry.assertion("toda:adopted:prop5.1:finite_dimensional").content
    assert isinstance(claim, TodaProp51FiniteDimensionalStatement)
    return claim


def _delta():
    return TodaDeltaInjectiveStatement(
        TodaDeltaMap(TodaPrimaryGroup(5, 5), TodaPrimaryGroup(3, 2))
    )


def _hopf():
    return TodaHopfInvariantSurjectiveStatement(
        TodaHopfInvariantMap(TodaPrimaryGroup(6, 3), TodaPrimaryGroup(6, 5))
    )


def test_r3f_delta_is_one_unproved_source_goal():
    claim = _source()
    option, = expand_registered_ehp_terminal_goal(_delta(), (claim,))
    assert option.subgoals == (claim,)
    assert option.rule.premise_patterns[0].proof_rule is ProofRule.INFERENCE


def test_r3f_hopf_has_exact_nu_prime_relation_goal_not_a_fact():
    claim = _source()
    option, = expand_registered_ehp_terminal_goal(_hopf(), (claim,))
    assert len(option.subgoals) == 2
    assert option.subgoals[1] == claim
    assert type(option.subgoals[0]).__name__ == "Relation"
    assert "ν′" in repr(option.subgoals[0])
    assert all(pattern.proof_rule is ProofRule.INFERENCE for pattern in option.rule.premise_patterns)


def test_r3f_terminal_rules_still_reject_screened_given_directly():
    claim = _source()
    for goal in (_delta(), _hopf()):
        option, = expand_registered_ehp_terminal_goal(goal, (claim,))
        given = ProofStep(claim, (), ProofRule.GIVEN)
        candidates = (given,) if len(option.subgoals) == 1 else (
            ProofStep(option.subgoals[0], (), ProofRule.GIVEN), given
        )
        assert find_inference_matches_for_rule(option.rule, candidates) == ()


def test_r3f_production_matcher_accepts_typed_derived_goals_in_isolation():
    claim = _source()
    for goal in (_delta(), _hopf()):
        option, = expand_registered_ehp_terminal_goal(goal, (claim,))
        # Synthetic fixture only: actual application must reconstruct these
        # ProofSteps with mathematical ancestors, not use this test's values.
        steps = tuple(ProofStep(x, (), ProofRule.INFERENCE) for x in option.subgoals)
        matches = find_inference_matches_for_rule(option.rule, steps)
        assert len(matches) == 1
        assert apply_inference_match(matches[0]).conclusion == goal


def test_r3f_no_prior_cited_composite_means_no_proposals():
    assert expand_registered_ehp_terminal_goal(_delta(), ()) == ()
    assert expand_registered_ehp_terminal_goal(_hopf(), ()) == ()


def test_r3f_ambiguous_source_is_rejected():
    source = _source()
    assert expand_registered_ehp_terminal_goal(_delta(), (source, source)) == ()
    assert expand_registered_ehp_terminal_goal(_hopf(), (source, source)) == ()


def test_r3f_unrelated_goals_do_not_create_proposals():
    source = _source()
    assert expand_registered_ehp_terminal_goal(object(), (source,)) == ()
    assert expand_registered_ehp_terminal_goal("H is onto", (source,)) == ()


def test_r3f_invalid_context_type_is_rejected():
    with pytest.raises(TypeError, match="tuple"):
        expand_registered_ehp_terminal_goal(_delta(), [_source()])

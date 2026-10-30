"""Focused typed EHP short-exact rule and real provenance regression tests."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import (
    TodaEHPExactnessWindow,
    TodaHopfInvariantMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase171_r2j_r4_r5_short_exact_sequence.audit import (
    _cited_prop42_source,
    _git,
    build_short_exact_proof,
)
from phase171_r2j_r4_r5_short_exact_sequence.source import (
    EHPShortExactSequence,
    ehp_short_exact_rule,
    expand_ehp_short_exact,
    short_exact_from_ehp,
)
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from proof import ProofRule, ProofStep, find_inference_matches_for_rule
from toda_rules import TodaProp42ExactnessStatement


def _premises():
    a = TodaPrimaryGroup(5, 2)
    b = TodaPrimaryGroup(6, 3)
    c = TodaPrimaryGroup(6, 5)
    injection = MapInjective(TodaSuspensionMap(a, b))
    exact = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        a, b, c, EHP_E_MAP, EHP_H_MAP,
    ))
    projection = MapSurjective(TodaHopfInvariantMap(b, c))
    return injection, exact, projection


def test_valid_ehp_window_and_maps_propose_one_short_exact_inference():
    inputs = _premises()
    assert prop42_exactness_indices(inputs[1]) == (2, 6, "e_h")
    goal = short_exact_from_ehp(*inputs)
    assert isinstance(goal, EHPShortExactSequence)
    assert goal.source_group == TodaPrimaryGroup(5, 2)
    assert goal.middle_group == TodaPrimaryGroup(6, 3)
    assert goal.target_group == TodaPrimaryGroup(6, 5)
    proposals = expand_ehp_short_exact(goal)
    assert len(proposals) == 1
    assert proposals[0].subgoals == inputs


def test_rule_produces_checked_inference_from_three_inferred_steps():
    inputs = _premises()
    goal = short_exact_from_ehp(*inputs)
    assert goal is not None
    rules = ehp_short_exact_rule(goal)
    premises = tuple(ProofStep(value, (), ProofRule.INFERENCE) for value in inputs)
    matches = find_inference_matches_for_rule(rules, premises)
    assert len(matches) == 1
    derived = derive_inference_proof_step(matches[0])
    assert derived.rule is ProofRule.INFERENCE
    assert derived.conclusion == goal
    assert derived.premises == premises


def test_given_exactness_or_map_properties_are_not_admitted_as_inference():
    inputs = _premises()
    goal = short_exact_from_ehp(*inputs)
    assert goal is not None
    rule = ehp_short_exact_rule(goal)
    for index in range(3):
        steps = tuple(ProofStep(
            statement, (), ProofRule.GIVEN if position == index else ProofRule.INFERENCE,
        ) for position, statement in enumerate(inputs))
        assert find_inference_matches_for_rule(rule, steps) == ()


def test_wrong_suspension_or_hopf_endpoints_fail_closed():
    injection, exact, projection = _premises()
    wrong_e = replace(injection, map=TodaSuspensionMap(
        TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 4),
    ))
    wrong_h = replace(projection, map=TodaHopfInvariantMap(
        TodaPrimaryGroup(6, 4), TodaPrimaryGroup(6, 5),
    ))
    assert short_exact_from_ehp(wrong_e, exact, projection) is None
    assert short_exact_from_ehp(injection, exact, wrong_h) is None


def test_invalid_exactness_or_wrong_ehp_map_names_fail_closed():
    injection, exact, projection = _premises()
    wrong = replace(exact, window=replace(
        exact.window, first_map=EHP_DELTA_MAP,
    ))
    assert short_exact_from_ehp(injection, wrong, projection) is None
    bad_group = replace(exact, window=replace(
        exact.window, target_term=TodaPrimaryGroup(7, 5),
    ))
    assert short_exact_from_ehp(injection, bad_group, projection) is None
    assert short_exact_from_ehp(injection, exact, object()) is None


def test_unrelated_sequence_is_rejected_and_reordered_premises_are_matched():
    inputs = _premises()
    goal = short_exact_from_ehp(*inputs)
    assert goal is not None
    incorrect = replace(goal, middle_group=TodaPrimaryGroup(7, 3))
    assert expand_ehp_short_exact(incorrect) == ()

    rule = ehp_short_exact_rule(goal)
    steps = tuple(ProofStep(item, (), ProofRule.INFERENCE) for item in inputs)
    reordered = (steps[2], steps[1], steps[0])
    matches = find_inference_matches_for_rule(rule, reordered)
    assert len(matches) == 1
    assert matches[0].premises == steps
    result = derive_inference_proof_step(matches[0])
    assert result.rule is ProofRule.INFERENCE
    assert result.conclusion == goal
    assert result.premises == steps

    wrong_injection = ProofStep(
        MapInjective(TodaSuspensionMap(
            TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 4),
        )),
        (),
        ProofRule.INFERENCE,
    )
    assert find_inference_matches_for_rule(
        rule, (steps[2], steps[1], wrong_injection),
    ) == ()
    assert expand_ehp_short_exact(object()) == ()


def test_real_proposition42_source_is_screened_and_unique():
    screened, _, citing = _screened_context()
    link = _cited_prop42_source(screened, citing)
    assert link.step.rule is ProofRule.GIVEN
    assert not link.step.premises
    assert link.assertion_id.endswith("adopted:assertion:prop42:general")


def test_read_only_git_guard():
    with pytest.raises(ValueError):
        _git("reset", "--hard")


def test_real_short_exact_proof_has_full_inferred_parentage():
    root, nodes, report = build_short_exact_proof()
    assert root.rule is ProofRule.INFERENCE
    assert len(root.premises) == 3
    assert all(parent.rule is ProofRule.INFERENCE for parent in root.premises)
    assert report["status"] == "INFERRED"
    assert report["new_given_added"] == 0
    assert report["order_four_proven"] is False
    assert report["pi63_group_proven"] is False
    assert report["given_leaves"] >= 3
    assert sum(node.rule is ProofRule.INFERENCE for node in nodes) >= 3

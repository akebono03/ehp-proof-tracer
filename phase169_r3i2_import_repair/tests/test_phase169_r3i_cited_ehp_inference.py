"""Focused R3I: cited premises yield new INFERENCE, never counterfeit GIVEN."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r14_r5_ehp_connection import (
    expand_cited_ehp_terminal_goal,
    expand_registered_ehp_terminal_goal,
)
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import ProofRule, find_inference_matches_for_rule
from toda_rules import TodaDeltaInjectiveStatement, TodaHopfInvariantSurjectiveStatement


@pytest.fixture(scope="module")
def actual():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=2)
    assert len(goals) == 1
    goal = goals[0]
    citing = resolve_specialized_goal_citing_id(bridge, goal)
    assert citing == "shared:0:boundary:Proposition 5.3:pi5_3_group_relation"
    contexts = []
    upper = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=contexts.append,
    )
    assert len(contexts) == 1
    context = contexts[0]
    given = tuple(
        link.step for link in context.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    hopf = TodaHopfInvariantSurjectiveStatement(
        TodaHopfInvariantMap(TodaPrimaryGroup(6, 3), TodaPrimaryGroup(6, 5)),
    )
    delta = TodaDeltaInjectiveStatement(
        TodaDeltaMap(TodaPrimaryGroup(5, 5), TodaPrimaryGroup(3, 2)),
    )
    return bridge, context, goal, citing, upper, given, (hopf, delta)


def test_r3i_only_exact_screened_claims_propose_cited_rules(actual):
    _, _, _, _, _, given, goals = actual
    sources = tuple(step.conclusion for step in given)
    for goal in goals:
        proposals = expand_cited_ehp_terminal_goal(goal, sources)
        assert len(proposals) == 1
        option = proposals[0]
        assert all(pattern.proof_rule is ProofRule.GIVEN for pattern in option.rule.premise_patterns)
        assert option.rule.conclusion_builder is not None
        assert option.rule.match_guard is not None
        assert len(option.subgoals) == len(option.rule.premise_patterns)


def test_r3i_derived_terminal_steps_have_exact_cited_ancestors(actual):
    _, _, _, _, _, given, goals = actual
    source_claims = tuple(step.conclusion for step in given)
    for goal in goals:
        option, = expand_cited_ehp_terminal_goal(goal, source_claims)
        prerequisites = tuple(
            next(step for step in given if type(step.conclusion) is type(child)
                 and step.conclusion == child)
            for child in option.subgoals
        )
        matches = find_inference_matches_for_rule(option.rule, prerequisites)
        assert len(matches) == 1
        inferred = derive_inference_proof_step(matches[0])
        assert inferred.rule is ProofRule.INFERENCE
        assert inferred.conclusion == goal
        assert inferred.premises == prerequisites
        assert all(step.rule is ProofRule.GIVEN and not step.premises for step in inferred.premises)


def test_r3i_historical_inference_only_rules_remain_intact(actual):
    _, _, _, _, _, given, goals = actual
    source_claims = tuple(step.conclusion for step in given)
    for goal in goals:
        original, = expand_registered_ehp_terminal_goal(goal, source_claims)
        assert all(p.proof_rule is ProofRule.INFERENCE for p in original.rule.premise_patterns)
        cited, = expand_cited_ehp_terminal_goal(goal, source_claims)
        assert cited.rule is not original.rule
        assert cited.rule.match_guard.__code__ is original.rule.match_guard.__code__
        assert cited.rule.conclusion_builder.__code__ is original.rule.conclusion_builder.__code__


def test_r3i_missing_source_does_not_create_a_premise(actual):
    _, _, _, _, _, given, goals = actual
    sources = tuple(step.conclusion for step in given)
    hopf, delta = goals
    actual_hopf_relation = expand_registered_ehp_terminal_goal(hopf, sources)[0].subgoals[0]
    without_hopf = tuple(source for source in sources if source != actual_hopf_relation)
    assert expand_cited_ehp_terminal_goal(hopf, without_hopf) == ()
    from toda_rules import TodaProp51FiniteDimensionalStatement
    without_prop51 = tuple(source for source in sources
                           if not isinstance(source, TodaProp51FiniteDimensionalStatement))
    assert expand_cited_ehp_terminal_goal(delta, without_prop51) == ()
    assert expand_cited_ehp_terminal_goal(hopf, without_prop51) == ()


def test_r3i_tampered_or_duplicate_citation_is_rejected(actual):
    _, _, _, _, _, given, goals = actual
    sources = tuple(step.conclusion for step in given)
    hopf = goals[0]
    actual_hopf = expand_registered_ehp_terminal_goal(hopf, sources)[0].subgoals[0]
    wrong_hopf = replace(actual_hopf, rhs="not-eta5")
    tampered = tuple(wrong_hopf if source == actual_hopf else source for source in sources)
    assert expand_cited_ehp_terminal_goal(hopf, tampered) == ()
    assert expand_cited_ehp_terminal_goal(hopf, sources + (actual_hopf,)) == ()


def test_r3i_unrelated_goals_and_bad_input_fail_closed(actual):
    _, _, _, _, _, given, _ = actual
    sources = tuple(step.conclusion for step in given)
    assert expand_cited_ehp_terminal_goal("not a mathematical goal", sources) == ()
    with pytest.raises(TypeError, match="tuple"):
        expand_cited_ehp_terminal_goal("not a mathematical goal", list(sources))


def test_r3i_real_recursive_proof_of_terminal_goals(actual):
    _, screened, goal, citing, _, _, terminals = actual
    provider = shared_expansion_provider(screened, proof_target=goal)
    for terminal in terminals:
        step = reconstruct_registered_goal(
            terminal, screened, citing, provider,
            lookup_mode="typed_reference_publication",
        )
        assert step.rule is ProofRule.INFERENCE
        assert step.conclusion == terminal
        assert all(p.rule is ProofRule.GIVEN for p in step.premises)
        assert len(step.premises) in (1, 2)
        assert step.inference_rule is not None
        assert step.inference_rule.name.startswith("cited prior sources:")


def test_r3i_lower_completed_proof_not_regressed(actual):
    bridge, _, _, _, upper, _, _ = actual
    lower = search_group_from_registered_goal(n=2, k=2, bridge=bridge)
    assert lower.status is ProofSearchStatus.COMPLETE
    assert upper.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.COMPLETE)

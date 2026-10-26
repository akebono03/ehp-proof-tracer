"""Focused R3U proof-boundary checks, using the actually screened bridge."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from phase165_r14_r5_ehp_connection import expand_cited_ehp_terminal_goal
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase165_r57_r20_general_specialization import specialize_typed_statement
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import ProofRule, Relation
from toda_rules import TodaDeltaInjectiveStatement, TodaProp51FiniteDimensionalStatement


@pytest.fixture(scope="module")
def actual():
    bridge = build_shared_typed_bridge()
    targets = registered_group_goal_candidates(bridge, n=3, k=2)
    assert len(targets) == 1
    target = targets[0]
    citing = resolve_specialized_goal_citing_id(bridge, target)
    contexts = []
    proof = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=contexts.append,
    )
    assert len(contexts) == 1
    context = contexts[0]
    available = tuple(
        link.step.conclusion for link in context.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    goal = TodaDeltaInjectiveStatement(
        TodaDeltaMap(TodaPrimaryGroup(5, 5), TodaPrimaryGroup(3, 2))
    )
    return bridge, context, target, citing, proof, available, goal


def test_delta_expansion_contains_cited_prop51_and_derived_diagonal(actual):
    _, _, _, _, _, available, goal = actual
    options = expand_cited_ehp_terminal_goal(goal, available)
    assert len(options) == 1
    option = options[0]
    assert len(option.subgoals) == 2
    assert isinstance(option.subgoals[0], TodaProp51FiniteDimensionalStatement)
    diagonal = option.subgoals[1]
    assert isinstance(diagonal, Relation)
    assert diagonal.lhs == goal.map.source_group
    assert [p.proof_rule for p in option.rule.premise_patterns] == [
        ProofRule.GIVEN, ProofRule.INFERENCE,
    ]
    sources = tuple(
        source for source in available
        if specialize_typed_statement(source, diagonal) is not None
    )
    assert len(sources) == 1


def test_actual_delta_proof_cites_51_and_derives_55_from_51(actual):
    _, context, target, citing, _, _, goal = actual
    provider = shared_expansion_provider(context, proof_target=target)
    result = reconstruct_registered_goal(
        goal, context, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    assert result.rule is ProofRule.INFERENCE
    assert result.conclusion == goal
    assert len(result.premises) == 2
    cited, diagonal = result.premises
    assert cited.rule is ProofRule.GIVEN
    assert isinstance(cited.conclusion, TodaProp51FiniteDimensionalStatement)
    assert diagonal.rule is ProofRule.INFERENCE
    assert len(diagonal.premises) == 1
    assert diagonal.premises[0].rule is ProofRule.GIVEN
    assert diagonal.premises[0].inference_rule.literature_reference.locator == "(5.1)"


def test_no_uncited_diagonal_or_wrong_source_can_prove_delta(actual):
    _, _, _, _, _, available, goal = actual
    option, = expand_cited_ehp_terminal_goal(goal, available)
    source = next(s for s in available if specialize_typed_statement(s, option.subgoals[1]) is not None)
    without_51 = tuple(s for s in available if s != source)
    assert expand_cited_ehp_terminal_goal(goal, without_51) == ()
    wrong = replace(option.subgoals[0], pi3_2_group_relation="not the cited group")
    with_wrong_prop = tuple(wrong if s == option.subgoals[0] else s for s in available)
    assert expand_cited_ehp_terminal_goal(goal, with_wrong_prop) == ()


def test_complete_pi53_proof_has_51_diagonal_in_delta_ancestry(actual):
    _, context, _, _, result, _, goal = actual
    assert result.status is ProofSearchStatus.COMPLETE
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    model = build_linked_proof_narrative_model(result, context)
    matching = [step for step in model.steps if step.conclusion == goal]
    assert len(matching) == 1
    delta = matching[0]
    assert len(delta.premises) == 2
    derived = delta.premises[1]
    assert isinstance(derived.conclusion, Relation)
    assert derived.conclusion.lhs == goal.map.source_group
    assert derived.rule is ProofRule.INFERENCE
    assert derived.premises[0].inference_rule.literature_reference.locator == "(5.1)"
    refs = [c.reference.locator for c in model.citations]
    assert "(5.1)" in refs
    assert "Proposition 5.1" in refs


def test_historical_rule_factory_remains_unmodified(actual):
    _, _, _, _, _, available, goal = actual
    from phase165_r14_r5_ehp_connection import expand_registered_ehp_terminal_goal
    old, = expand_registered_ehp_terminal_goal(goal, available)
    new, = expand_cited_ehp_terminal_goal(goal, available)
    assert len(old.rule.premise_patterns) == 1
    assert len(new.rule.premise_patterns) == 2
    assert old.rule.conclusion_builder is not new.rule.conclusion_builder
    assert old.rule.match_guard is not new.rule.match_guard

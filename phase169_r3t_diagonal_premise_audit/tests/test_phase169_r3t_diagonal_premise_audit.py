"""Read-only tests for a typed, literature-backed pi5^5 goal."""
from __future__ import annotations

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase165_r57_r20_general_specialization import specialize_typed_statement
from phase169_r3t_diagonal_premise_audit.audit import diagonal_pi55_goal
from proof import Relation, RelationType


def test_pi55_goal_is_concrete_and_not_a_source_step():
    goal = diagonal_pi55_goal()
    assert isinstance(goal, Relation)
    assert goal.relation_type is RelationType.EQUALITY
    assert goal.lhs == TodaPrimaryGroup(5, 5)
    assert isinstance(goal.rhs, FreeCyclicGroup)
    assert goal.rhs.generator.generator == GeneratorSymbol(family="ι", index=5)


def test_unrelated_fixed_relation_cannot_specialize_pi55():
    wrong = Relation(
        TodaPrimaryGroup(4, 4),
        FreeCyclicGroup(
            HomotopyElement(name="ι_4", dimension=4, generator=GeneratorSymbol(family="ι", index=4))
        ),
        relation_type=RelationType.EQUALITY,
    )
    assert specialize_typed_statement(wrong, diagonal_pi55_goal()) is None


def test_screened_cited_diagonal_specialization_is_available():
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
    from phase165_r57_r20_general_specialization import expand_cited_general_specialization
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=2)
    assert len(goals) == 1
    contexts = []
    search_group_from_registered_goal(n=3, k=2, bridge=bridge, context_sink=contexts.append)
    assert len(contexts) == 1
    screened = contexts[0]
    available = tuple(
        link.step.conclusion
        for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
    )
    diagonal = diagonal_pi55_goal()
    proposals = expand_cited_general_specialization(diagonal, available)
    assert len(proposals) >= 1, "Cited (5.1) specialization not available: inspect R3T report"
    assert all(len(item.subgoals) == 1 and item.subgoals[0] in available for item in proposals)

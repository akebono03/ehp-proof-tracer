"""R12-R5 focused generic (not pi43-specific) search and proof checks."""
import pytest

from expression import eta
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r12_r5_structure_bridge import finite_cyclic_structure_as_relation_inference_rule
from phase165_r57_r26_generic_search_connection import build_generic_backward_expansion_provider
from phase165_r8_rule_provider import DEFAULT_RULE_MODULES, discover_inference_rules
from phase165_r10_rule_registry import build_rule_registry
from proof import (
    ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_matches_for_rule,
)


def _goal(n=3, order=2):
    return Relation(
        lhs=TodaPrimaryGroup(n + 1, n),
        rhs=FiniteCyclicGroup(order, eta(n)),
        relation_type=RelationType.EQUALITY,
    )


def test_registered_automatically_in_both_catalogs():
    rule_id = "phase165_r12_r5_structure_bridge.finite_cyclic_structure_as_relation_inference_rule"
    registry = build_rule_registry(DEFAULT_RULE_MODULES)
    entry = registry.by_id(rule_id)
    rules, _ = discover_inference_rules()
    assert entry.rule.name in [r.name for r in rules]
    assert "phase165_r12_r2_quotient_rules" in DEFAULT_RULE_MODULES


def test_reverse_goal_creates_typed_unproved_subgoal():
    goal = _goal()
    rule = finite_cyclic_structure_as_relation_inference_rule()
    proposals = build_generic_backward_expansion_provider((rule,))(goal)
    assert len(proposals) == 1
    assert proposals[0].subgoals == (CyclicStructureStatement(goal.lhs, eta(3), 2),)


def test_rule_reuses_different_groups_orders_and_generators():
    rule = finite_cyclic_structure_as_relation_inference_rule()
    for n, order in ((3, 2), (5, 4), (9, 7)):
        goal = _goal(n, order)
        proposals = build_generic_backward_expansion_provider((rule,))(goal)
        assert len(proposals) == 1
        assert proposals[0].subgoals == (CyclicStructureStatement(goal.lhs, eta(n), order),)


def test_forward_checked_proof_step_preserves_parent():
    rule = finite_cyclic_structure_as_relation_inference_rule()
    goal = _goal()
    given = ProofStep(
        conclusion=CyclicStructureStatement(goal.lhs, eta(3), 2),
        premises=(), rule=ProofRule.GIVEN,
    )
    matches = find_inference_matches_for_rule(rule, (given,))
    assert len(matches) == 1
    inferred = apply_inference_match(matches[0])
    assert inferred.conclusion == goal
    assert inferred.rule is ProofRule.INFERENCE
    assert inferred.premises == (given,)
    assert inferred.inference_rule is rule


def test_without_a_proved_premise_no_forward_match():
    rule = finite_cyclic_structure_as_relation_inference_rule()
    assert find_inference_matches_for_rule(rule, ()) == ()
    with pytest.raises(ValueError):
        CyclicStructureStatement(_goal().lhs, eta(3), 0)


def test_target_is_not_directly_registered_as_fact():
    rule = finite_cyclic_structure_as_relation_inference_rule()
    assert rule.premise_patterns
    assert rule.literature_reference is None
    assert rule.conclusion_builder is None

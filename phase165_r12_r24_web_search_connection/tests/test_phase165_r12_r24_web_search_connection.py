"""Focused generic inversion and fail-closed Web connector checks."""
from __future__ import annotations

from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase165_r12_r24_web_search_connection import expand_finite_cyclic_relation
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from proof import Relation
from toda_rules import toda_eta_family_definition_statement


def test_finite_cyclic_goal_reverse_generates_only_bound_structure():
    group = TodaPrimaryGroup(4, 3)
    eta = toda_eta_family_definition_statement(3).element
    goal = Relation(group, FiniteCyclicGroup(2, eta))
    option, = expand_finite_cyclic_relation(goal)
    assert option.subgoals == (CyclicStructureStatement(group, eta, 2),)
    assert option.rule.name == 'finite cyclic structure gives group relation'


def test_nonfinite_group_goal_is_not_accepted():
    group = TodaPrimaryGroup(3, 2)
    eta = toda_eta_family_definition_statement(2).element
    assert expand_finite_cyclic_relation(Relation(group, FreeCyclicGroup(eta))) == ()
    assert expand_finite_cyclic_relation(group) == ()


def test_same_rule_works_for_other_target_and_order():
    group = TodaPrimaryGroup(8, 5)
    generator = toda_eta_family_definition_statement(5).element
    option, = expand_finite_cyclic_relation(Relation(group, FiniteCyclicGroup(4, generator)))
    assert option.subgoals == (CyclicStructureStatement(group, generator, 4),)

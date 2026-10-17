"""Focused root-specialization gate tests for Phase 165 R4-R12."""
import pytest
from expression import GeneratorSymbol, HomotopyElement, ScalarSum, ScalarSymbol
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from phase165_r57_r11_proof_order_gate import retain_ordered_root_expansions
from proof import InferenceRule, Relation, RelationType


def _goals():
    n = ScalarSymbol('n')
    concrete = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(
        2, HomotopyElement('η_3', 3, 4, 3, GeneratorSymbol('η', 3)),
    ), RelationType.EQUALITY)
    symbolic = Relation(TodaPrimaryGroup(ScalarSum(n, 1), n), FiniteCyclicGroup(
        2, HomotopyElement('η_n', n, ScalarSum(n, 1), n, GeneratorSymbol('η', n)),
    ), RelationType.EQUALITY)
    return concrete, symbolic


@pytest.mark.parametrize('rule_name', [
    'Toda Proposition 5.1 generic higher-eta specialization',
    'generic cited typed scalar specialization',
])
def test_matching_symbolic_source_retained(rule_name):
    goal, source = _goals()
    candidate = GoalExpansion(InferenceRule(rule_name), (source,))
    assert retain_ordered_root_expansions(goal, goal, (candidate,)) == (candidate,)


def test_concrete_self_citation_still_rejected():
    goal, _ = _goals()
    candidate = GoalExpansion(InferenceRule('generic cited typed scalar specialization'), (goal,))
    assert retain_ordered_root_expansions(goal, goal, (candidate,)) == ()


def test_unrelated_rule_still_rejected():
    goal, source = _goals()
    candidate = GoalExpansion(InferenceRule('unrelated rule'), (source,))
    assert retain_ordered_root_expansions(goal, goal, (candidate,)) == ()


def test_nonmatching_symbolic_source_still_rejected():
    goal, source = _goals()
    other = Relation(TodaPrimaryGroup(5, 4), goal.rhs, RelationType.EQUALITY)
    candidate = GoalExpansion(InferenceRule('generic cited typed scalar specialization'), (source,))
    assert retain_ordered_root_expansions(other, other, (candidate,)) == ()

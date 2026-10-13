from dataclasses import dataclass
import pytest

from phase165_r14_r5_ehp_connection import (
    adapt_registered_goal_expansion, expand_registered_ehp_goal,
)
from phase165_r3_recursive_search import GoalExpansion


@dataclass(frozen=True)
class FakeExpansion:
    goal: object
    inference_rule: object
    subgoals: tuple[object, ...]


def test_existing_expansion_converts_without_creating_steps():
    target = "T"
    parent = FakeExpansion(target, "RULE", ("P", "Q"))
    options = adapt_registered_goal_expansion(target, lambda g: parent)
    assert options == (GoalExpansion("RULE", ("P", "Q")),)


def test_absent_expansion_is_empty():
    assert adapt_registered_goal_expansion("G", lambda g: None) == ()


def test_mismatched_goal_is_rejected():
    with pytest.raises(ValueError, match="mismatch"):
        adapt_registered_goal_expansion(
            "G", lambda g: FakeExpansion("wrong", "R", ())
        )


def test_invalid_premises_are_rejected():
    with pytest.raises(TypeError, match="tuple"):
        adapt_registered_goal_expansion(
            "G", lambda g: FakeExpansion("G", "R", ["P"])
        )


def test_missing_rule_is_rejected():
    with pytest.raises(ValueError, match="rule missing"):
        adapt_registered_goal_expansion(
            "G", lambda g: FakeExpansion("G", None, ())
        )


def test_unrecognized_goal_has_no_fabricated_expansion():
    assert expand_registered_ehp_goal(object()) == ()

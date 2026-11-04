"""No-data-loss identity checks; display equality must not rewrite typed Goals."""
from __future__ import annotations

from dataclasses import dataclass

from phase173_r4_r15r17r3_goal_contract_audit.audit import (
    inspect_goal_pairs,
    reversed_relation,
    stable_equal,
)


@dataclass(frozen=True)
class NamedGoal:
    name: str


@dataclass(frozen=True)
class AlternativeGoal:
    name: str


@dataclass(frozen=True)
class RelationStub:
    lhs: str
    rhs: str
    relation_type: str = "equality"


def test_same_latex_different_types_are_not_typed_duplicates() -> None:
    goals = (NamedGoal("a"), AlternativeGoal("a"))
    audit = inspect_goal_pairs(goals, lambda goal: "$a$")
    assert audit["count"] == 2
    assert len(audit["goals"]) == 2
    assert audit["paired_observations"] == [{
        "first": 1, "second": 2, "same_display": True,
        "same_type_and_equal": False, "reversed_relation": False,
        "same_object": False,
    }]
    assert goals == (NamedGoal("a"), AlternativeGoal("a"))


def test_identical_typed_values_are_reported_but_not_coalesced() -> None:
    goals = (NamedGoal("a"), NamedGoal("a"))
    audit = inspect_goal_pairs(goals, lambda goal: "$a$")
    assert audit["count"] == 2
    assert len(audit["goals"]) == 2
    assert audit["paired_observations"][0]["same_type_and_equal"] is True
    assert audit["paired_observations"][0]["same_object"] is False


def test_reversed_relation_is_not_reinterpreted_as_one_obligation() -> None:
    a = RelationStub("X", "Y")
    b = RelationStub("Y", "X")
    assert reversed_relation(a, b) is True
    assert stable_equal(a, b) is False
    audit = inspect_goal_pairs((a, b), lambda goal: f"{goal.lhs}={goal.rhs}")
    assert audit["paired_observations"][0]["reversed_relation"] is True
    assert len(audit["goals"]) == 2


def test_distinct_math_does_not_count_as_display_collision() -> None:
    audit = inspect_goal_pairs((NamedGoal("a"), NamedGoal("b")), lambda goal: goal.name)
    assert audit["paired_observations"] == []


def test_non_tuple_goal_collection_fails_closed() -> None:
    try:
        inspect_goal_pairs([NamedGoal("a")], lambda goal: goal.name)
    except TypeError as error:
        assert "tuple" in str(error)
    else:
        raise AssertionError("non-tuple open_goals must fail")

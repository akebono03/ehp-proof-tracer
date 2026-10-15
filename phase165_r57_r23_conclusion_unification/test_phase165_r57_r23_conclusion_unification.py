"""R23 focused conclusion-unification tests (no whole-suite pytest)."""
from __future__ import annotations

from dataclasses import dataclass

import pytest

from phase165_r57_r23_conclusion_unification import unify_inference_conclusion
from proof import (
    ImageStatement,
    InferenceRule,
    PatternVariable,
    Relation,
    RelationType,
    VariableBinding,
)


@dataclass(frozen=True)
class NestedStatement:
    lhs: object
    rhs: object


def test_r23_explicit_conclusion_pattern_unifies_typed_goal():
    source = PatternVariable("source")
    rule = InferenceRule(
        name="generic image conclusion",
        conclusion_pattern=ImageStatement(source, "image"),
    )
    result = unify_inference_conclusion(rule, ImageStatement("f", "image"))
    assert result is not None
    assert result.rule is rule
    assert result.bindings == (VariableBinding(source, "f"),)


def test_r23_nested_typed_patterns_and_tuples():
    group = PatternVariable("group")
    rule = InferenceRule(
        name="nested typed conclusion",
        conclusion_pattern=NestedStatement(
            Relation(group, "Z", RelationType.EQUALITY),
            (ImageStatement("E", group), "complete"),
        ),
    )
    goal = NestedStatement(
        Relation("pi", "Z", RelationType.EQUALITY),
        (ImageStatement("E", "pi"), "complete"),
    )
    result = unify_inference_conclusion(rule, goal)
    assert result is not None
    assert result.bindings == (VariableBinding(group, "pi"),)


def test_r23_repeated_variable_conflict_rejected():
    group = PatternVariable("group")
    rule = InferenceRule(
        name="shared variable",
        conclusion_pattern=NestedStatement(group, group),
    )
    assert unify_inference_conclusion(rule, NestedStatement("A", "B")) is None
    assert unify_inference_conclusion(rule, NestedStatement("A", "A")) is not None


def test_r23_wrong_type_and_relation_type_rejected():
    rule = InferenceRule(
        name="typed relation",
        conclusion_pattern=Relation("A", "B", RelationType.EQUALITY),
    )
    assert unify_inference_conclusion(rule, ImageStatement("A", "B")) is None
    assert unify_inference_conclusion(rule, Relation("A", "B", RelationType.ZERO)) is None


def test_r23_conclusion_builder_without_pattern_is_not_guessed():
    rule = InferenceRule(name="builder only", conclusion_builder=lambda premises: "A")
    assert unify_inference_conclusion(rule, "A") is None
    assert unify_inference_conclusion(InferenceRule(name="no pattern"), "A") is None


def test_r23_tuple_length_and_constant_mismatch_rejected():
    rule = InferenceRule(name="tuple", conclusion_pattern=("E", PatternVariable("n")))
    assert unify_inference_conclusion(rule, ("E", 3, 4)) is None
    assert unify_inference_conclusion(rule, ("H", 3)) is None


def test_r23_invalid_rule_type_rejected():
    with pytest.raises(TypeError, match="InferenceRule"):
        unify_inference_conclusion(object(), "A")

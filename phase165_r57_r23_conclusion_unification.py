"""Phase 165 R57-R23: typed conclusion unification for backward proposals.

This module matches an explicitly declared InferenceRule.conclusion_pattern.
It neither discovers rules nor constructs proof steps. A conclusion_builder alone
is intentionally not invertible and is not interpreted as a pattern.
"""
from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass

from proof import (
    InferenceRule,
    PatternVariable,
    VariableBinding,
    match_pattern_value,
    merge_variable_bindings,
    substitute_pattern_value,
)


@dataclass(frozen=True)
class ConclusionUnification:
    rule: InferenceRule
    goal: object
    bindings: tuple[VariableBinding, ...]


def _match_nested(pattern: object, goal: object) -> tuple[VariableBinding, ...] | None:
    if isinstance(pattern, PatternVariable):
        return match_pattern_value(pattern, goal)
    if isinstance(pattern, tuple):
        if not isinstance(goal, tuple) or len(pattern) != len(goal):
            return None
        parts = zip(pattern, goal)
    elif is_dataclass(pattern) and not isinstance(pattern, type):
        if type(pattern) is not type(goal):
            return None
        parts = ((getattr(pattern, field.name), getattr(goal, field.name))
                 for field in fields(pattern))
    else:
        return match_pattern_value(pattern, goal)
    bindings: tuple[VariableBinding, ...] = ()
    for left, right in parts:
        found = _match_nested(left, right)
        if found is None:
            return None
        merged = merge_variable_bindings(bindings + found)
        if merged is None:
            return None
        bindings = merged
    return bindings


def _instantiate_nested(pattern: object, bindings: tuple[VariableBinding, ...]) -> object:
    if isinstance(pattern, PatternVariable):
        return substitute_pattern_value(pattern, bindings)
    if isinstance(pattern, tuple):
        return tuple(_instantiate_nested(value, bindings) for value in pattern)
    if is_dataclass(pattern) and not isinstance(pattern, type):
        return type(pattern)(**{
            field.name: _instantiate_nested(getattr(pattern, field.name), bindings)
            for field in fields(pattern)
        })
    return substitute_pattern_value(pattern, bindings)


def unify_inference_conclusion(
    rule: InferenceRule, goal: object
) -> ConclusionUnification | None:
    """Match a typed goal against a rule's explicit conclusion pattern.

    No pattern means no reverse match. The returned bindings are candidates;
    proof validity still requires forward checking once premises are proved.
    """
    if not isinstance(rule, InferenceRule):
        raise TypeError("rule must be InferenceRule")
    pattern = rule.conclusion_pattern
    if pattern is None:
        return None
    bindings = _match_nested(pattern, goal)
    if bindings is None or _instantiate_nested(pattern, bindings) != goal:
        return None
    return ConclusionUnification(rule=rule, goal=goal, bindings=bindings)

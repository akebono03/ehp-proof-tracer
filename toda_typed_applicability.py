"""Typed inference-rule applicability over already established ProofSteps.

This does not turn unverified registry entries into premises and does not
execute any inference rule. It reports precisely matching rule applications.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from proof import InferenceRule, ProofStep, find_inference_matches_for_rule
from phase165_r8_rule_provider import discover_inference_rules


@dataclass(frozen=True)
class TypedApplicableRule:
    rule: InferenceRule
    matches: tuple[object, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.rule, InferenceRule):
            raise TypeError("rule must be an InferenceRule")
        if not isinstance(self.matches, tuple) or not self.matches:
            raise ValueError("matches must be a nonempty tuple")


def find_typed_applicable_rules(
    proven_steps: Iterable[ProofStep],
    *,
    rules: Iterable[InferenceRule] | None = None,
) -> tuple[TypedApplicableRule, ...]:
    """Find exact premise matches; never infer or execute a conclusion.

    Supplying rules allows deterministic, scoped use in unit tests and callers.
    If omitted, reuse the one shared Phase 165 rule-discovery catalog.
    """
    steps = tuple(proven_steps)
    if any(not isinstance(step, ProofStep) for step in steps):
        raise TypeError("proven_steps must contain only ProofStep values")
    if rules is None:
        catalog, _report = discover_inference_rules()
    else:
        catalog = tuple(rules)
    if any(not isinstance(rule, InferenceRule) for rule in catalog):
        raise TypeError("rules must contain only InferenceRule values")

    applicable = []
    for rule in catalog:
        matches = tuple(find_inference_matches_for_rule(rule, steps))
        if matches:
            applicable.append(TypedApplicableRule(rule=rule, matches=matches))
    return tuple(applicable)

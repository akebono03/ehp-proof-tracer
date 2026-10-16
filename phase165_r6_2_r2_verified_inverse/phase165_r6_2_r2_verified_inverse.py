"""Recover backward premises from existing verified typed witness steps.

No group number, Toda-specific generator, or new GIVEN step is constructed.
This provider supplements (but does not replace) symbolic inverse patterns.
"""
from __future__ import annotations

from phase165_r3_recursive_search import GoalExpansion
from proof import (
    InferenceRule, ProofStep, PremisePattern,
    apply_inference_match, find_inference_matches_for_rule,
    match_premise_pattern,
)


def reverse_rules_from_witnesses(
    goal: object,
    rules: tuple[InferenceRule, ...],
    witnesses: tuple[ProofStep, ...],
    *,
    max_combinations: int = 2048,
) -> tuple[GoalExpansion, ...]:
    """Return only reverse proposals independently checked by forward inference.

    Exhaustive candidate generation is bounded. If a search would exceed the
    budget, fail closed rather than pretending all candidates were inspected.
    A returned GoalExpansion remains a search proposal, not a new proof step.
    """
    if not isinstance(rules, tuple) or any(not isinstance(x, InferenceRule) for x in rules):
        raise TypeError("rules must be a tuple of InferenceRule")
    if not isinstance(witnesses, tuple) or any(not isinstance(x, ProofStep) for x in witnesses):
        raise TypeError("witnesses must be a tuple of ProofStep")
    if type(max_combinations) is not int or max_combinations <= 0:
        raise ValueError("max_combinations must be a positive integer")
    results: list[GoalExpansion] = []
    inspected = 0
    for rule in rules:
        if not rule.premise_patterns:
            continue
        buckets: list[tuple[ProofStep, ...]] = []
        for pattern in rule.premise_patterns:
            if not isinstance(pattern, PremisePattern):
                raise TypeError("rule contains a non-PremisePattern")
            bucket = tuple(step for step in witnesses
                           if match_premise_pattern(pattern, step) is not None)
            if not bucket:
                break
            buckets.append(bucket)
        if len(buckets) != len(rule.premise_patterns):
            continue
        count = 1
        for bucket in buckets:
            count *= len(bucket)
        if inspected + count > max_combinations:
            raise ValueError("generic witness inverse search budget exceeded")
        inspected += count
        # Each match is checked using the existing rule's guard, bindings,
        # and conclusion builder, not by comparing unverified string formulas.
        from itertools import product
        for candidate in product(*buckets):
            for match in find_inference_matches_for_rule(rule, candidate):
                if match.premises != candidate:
                    continue
                derived = apply_inference_match(match)
                if type(derived.conclusion) is not type(goal) or derived.conclusion != goal:
                    continue
                expansion = GoalExpansion(rule, tuple(x.conclusion for x in candidate))
                if not any(x.rule is expansion.rule and x.subgoals == expansion.subgoals
                           for x in results):
                    results.append(expansion)
    return tuple(results)

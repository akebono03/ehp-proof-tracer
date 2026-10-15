"""Phase 165 R57-R25: reverse typed premise instantiation.

Only concrete premise templates whose variables are bound by R23 are expanded.
A GoalExpansion is a search proposal, never a proof or a new GIVEN fact.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r3_recursive_search import GoalExpansion
from phase165_r57_r23_conclusion_unification import (
    _instantiate_nested,
    unify_inference_conclusion,
)
from phase165_r57_r24_candidate_discovery import DiscoveredRuleCandidate
from phase165_r8_rule_provider import _pattern_variable_names, _unresolved_pattern
from proof import PremisePattern, Relation


@dataclass(frozen=True)
class PremiseGenerationResult:
    """A validated proposal with its original catalog identity."""

    key: str
    expansion: GoalExpansion
    source: str


def generate_candidate_premises(
    candidate: DiscoveredRuleCandidate,
) -> PremiseGenerationResult | None:
    """Instantiate fully bound typed premise templates without guessing witnesses.

    None means that a specific candidate cannot yet be reversed. It does not
    assert that the goal is false or that the forward rule is inapplicable.
    """
    if not isinstance(candidate, DiscoveredRuleCandidate):
        raise TypeError("candidate must be DiscoveredRuleCandidate")

    matched = candidate.unification
    verified = unify_inference_conclusion(matched.rule, matched.goal)
    if verified is None or verified.bindings != matched.bindings:
        return None

    if not matched.rule.premise_patterns:
        return None
    bound_names = {item.variable.name for item in verified.bindings}
    subgoals: list[object] = []
    for premise in matched.rule.premise_patterns:
        if not isinstance(premise, PremisePattern):
            return None
        if premise.relation_pattern is not None and premise.statement_pattern is not None:
            return None
        template = (
            premise.relation_pattern if premise.relation_pattern is not None
            else premise.statement_pattern
        )
        if template is None or _unresolved_pattern(template) and not _pattern_variable_names(template).issubset(bound_names):
            return None
        concrete = _instantiate_nested(template, verified.bindings)
        if _unresolved_pattern(concrete):
            return None
        if premise.statement_type is not None and not isinstance(concrete, premise.statement_type):
            return None
        if premise.relation_pattern is not None and not isinstance(concrete, Relation):
            return None
        if premise.relation_type is not None:
            if not isinstance(concrete, Relation) or concrete.relation_type is not premise.relation_type:
                return None
        subgoals.append(concrete)

    return PremiseGenerationResult(
        key=candidate.key,
        expansion=GoalExpansion(rule=matched.rule, subgoals=tuple(subgoals)),
        source=candidate.source,
    )


def generate_discovered_premises(
    candidates: tuple[DiscoveredRuleCandidate, ...],
) -> tuple[PremiseGenerationResult, ...]:
    """Generate ordered proposals; candidates not invertible are skipped."""
    if not isinstance(candidates, tuple):
        raise TypeError("candidates must be a tuple")
    output: list[PremiseGenerationResult] = []
    for candidate in candidates:
        generated = generate_candidate_premises(candidate)
        if generated is not None:
            output.append(generated)
    return tuple(output)

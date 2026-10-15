"""R57-R26: connect R23/R24/R25 to the existing canonical backward search.

This adapter only emits typed GoalExpansion proposals. References and ProofSteps
remain exclusively under reconstruct_registered_goal's existing verification.
"""
from __future__ import annotations

from phase165_r3_recursive_search import GoalExpansion
from phase165_r57_r24_candidate_discovery import discover_explicit_goal_candidates
from phase165_r57_r25_premise_generation import generate_discovered_premises
from phase165_r8_rule_provider import discover_inference_rules
from proof import InferenceRule


def build_generic_backward_expansion_provider(
    rules: tuple[InferenceRule, ...] | None = None,
):
    """Create an immutable goal-to-expansions provider from existing rule factories.

    The factory inventory is read once rather than once for each recursive goal.
    Only explicitly invertible conclusion and premise patterns can contribute.
    """
    if rules is None:
        rules, _ = discover_inference_rules()
    if not isinstance(rules, tuple) or any(
        not isinstance(rule, InferenceRule) for rule in rules
    ):
        raise TypeError("rules must be a tuple of InferenceRule")

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        matches = discover_explicit_goal_candidates(rules, goal)
        results = generate_discovered_premises(matches)
        return tuple(result.expansion for result in results)

    return expand


def merge_backward_expansions(
    existing: tuple[GoalExpansion, ...],
    generic: tuple[GoalExpansion, ...],
) -> tuple[GoalExpansion, ...]:
    """Preserve existing provider order and suppress duplicate identical proposals.

    Different derivations stay distinct for the canonical ambiguity checker.
    """
    if not isinstance(existing, tuple) or not isinstance(generic, tuple):
        raise TypeError("expansions must be tuples")
    output: list[GoalExpansion] = []
    for expansion in existing + generic:
        if not isinstance(expansion, GoalExpansion):
            raise TypeError("expansions must contain GoalExpansion")
        if any(
            previous.rule is expansion.rule
            and previous.subgoals == expansion.subgoals
            for previous in output
        ):
            continue
        output.append(expansion)
    return tuple(output)

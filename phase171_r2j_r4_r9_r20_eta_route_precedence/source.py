"""Prefer the typed η specialization over an identical generic scalar route.

Both source-to-conclusion inference rules remain callable independently.
This helper removes only a redundant backward proposal that uses the *same*
screened source and target as the existing, mathematically checked η route.
It never constructs ProofSteps, adds GIVEN sources, or weakens uniqueness.
"""
from __future__ import annotations

from phase165_r3_recursive_search import GoalExpansion
from phase165_r57_r8_eta_specialization import expand_registered_eta_specialization

ETA_RULE = "Toda Proposition 5.1 generic higher-eta specialization"
SCALAR_RULE = "generic cited typed scalar specialization"


def prefer_specific_cited_eta_specialization(
    goal: object, available: tuple[object, ...],
    expansions: tuple[GoalExpansion, ...],
) -> tuple[GoalExpansion, ...]:
    """Suppress only the generic route shadowing a vetted exact η route.

    Require both candidates in the same expansion tuple and verify the
    specialized rule against available screened source conclusions. A
    different source or a different conclusion never becomes interchangeable.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if not isinstance(expansions, tuple):
        raise TypeError("expansions must be a tuple")
    if not all(isinstance(value, GoalExpansion) for value in expansions):
        raise TypeError("all proposals must be GoalExpansion instances")
    confirmed = expand_registered_eta_specialization(goal, available)
    concrete = tuple(
        item for item in expansions
        if getattr(item.rule, "name", None) == ETA_RULE
        and any(reference.subgoals == item.subgoals for reference in confirmed)
    )
    if not concrete:
        return expansions
    return tuple(
        item for item in expansions
        if not (
            getattr(item.rule, "name", None) == SCALAR_RULE
            and any(item.subgoals == specific.subgoals for specific in concrete)
        )
    )

"""Phase 165 R14: a real typed group goal and read-only production frontier.

This creates neither premises nor historical replay results.  It does not
assert mathematical verification of a Toda citation.
"""
from __future__ import annotations

from dataclasses import dataclass

from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from proof import Relation, RelationType
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r12_typed_binding import build_batch_typed_bindings
from phase165_goal_only_search import (
    GoalSearchIncompleteError,
    construct_registered_group_proof,
)
from unified_statement_registry import AssertionOrigin


@dataclass(frozen=True)
class TypedGoalFrontier:
    goal: Relation
    source_assertions: int
    typed_assertions: int
    eligible_assertions: int
    exact_registered_goal_matches: int
    status: str
    blocker: str


def build_free_cyclic_group_goal(n: int, k: int, generator: object) -> Relation:
    """General goal constructor; no pi_3^2-only proof rules or premises."""
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        raise ValueError("n must be an integer >= 2")
    if isinstance(k, bool) or not isinstance(k, int) or k < 0:
        raise ValueError("k must be a nonnegative integer")
    return Relation(
        lhs=TodaPrimaryGroup(group_dimension=n + k, sphere_dimension=n),
        rhs=FreeCyclicGroup(generator=generator),
        relation_type=RelationType.EQUALITY,
    )


def inspect_free_cyclic_goal(n: int, k: int, generator: object) -> TypedGoalFrontier:
    """Inspect actual registered data and refuse to guess a source or rule catalog."""
    goal = build_free_cyclic_group_goal(n, k, generator)
    bridge, _ = build_phase165_r5_manifest_bridge()
    source_bindings = build_batch_typed_bindings(bridge)
    matches = sum(
        1 for assertion in bridge.registry._assertions.values()
        if assertion.origin is AssertionOrigin.FIXED_STATEMENT
        and type(assertion.content) is type(goal)
        and assertion.content == goal
    )
    try:
        construct_registered_group_proof(n=n, k=k, goal=goal)
    except GoalSearchIncompleteError as exc:
        status = "UNRESOLVED"
        blocker = str(exc)
    else:
        raise RuntimeError("Unexpected proof without a verified bridge or rule catalog")
    return TypedGoalFrontier(
        goal=goal,
        source_assertions=len(source_bindings.records),
        typed_assertions=source_bindings.mathematically_typed,
        eligible_assertions=source_bindings.proof_eligible,
        exact_registered_goal_matches=matches,
        status=status,
        blocker=blocker,
    )

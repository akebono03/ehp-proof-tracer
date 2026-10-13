"""R14-R34: goal-first expansion for the existing strict registered search.

The unreviewed adopted-TeX leaves remain ineligible. This module never replays
R33's completed proof tree or invents GIVEN evidence.
"""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup, FreeCyclicGroup, TodaHopfInvariantMap
from hopf_facts import ETA_2, IOTA_3
from phase165_r14_r6_generic_iso import (
    GeneratorImage, MapIsomorphism, expand_generic_iso_goal,
)
from phase165_r14_r9_ehp_exactness import expand_generic_ehp_hopf_goal
from phase165_r14_r11_delta_zero import expand_delta_zero_from_suspension_iso
from phase165_r14_r14_diagonal_and_prop42 import expand_diagonal_suspension
from phase165_r14_r33_final_group import reverse_free_cyclic_transport_rule
from phase165_r3_recursive_search import (
    GoalExpansion, RegisteredGoalUnresolved, reconstruct_registered_goal,
)
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from proof import Relation


def pi32_goal() -> Relation:
    return Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))


def _hopf_map() -> TodaHopfInvariantMap:
    return TodaHopfInvariantMap(TodaPrimaryGroup(3, 2), TodaPrimaryGroup(3, 3))


def phase165_r34_expansions(goal: object) -> tuple[GoalExpansion, ...]:
    """Only backward inference proposals, not proofs or uncertified leaves."""
    if goal == pi32_goal():
        return (GoalExpansion(
            reverse_free_cyclic_transport_rule(),
            (
                MapIsomorphism(_hopf_map()),
                Relation(TodaPrimaryGroup(3, 3), FreeCyclicGroup(IOTA_3)),
                GeneratorImage(_hopf_map(), ETA_2, IOTA_3),
            ),
        ),)
    for provider in (
        expand_generic_iso_goal,
        expand_generic_ehp_hopf_goal,
        expand_delta_zero_from_suspension_iso,
        expand_diagonal_suspension,
    ):
        options = provider(goal)
        if options:
            if not isinstance(options, tuple) or not all(
                isinstance(option, GoalExpansion) for option in options
            ):
                raise TypeError("existing expansion provider contract violated")
            return options
    return ()


def trace_goal_frontier(root: object, limit: int = 80) -> dict:
    """Inspect dependencies independently of any existing ProofStep tree."""
    if type(limit) is not int or limit <= 0:
        raise ValueError("limit must be positive")
    queue = [root]
    visited = []
    internal = []
    leaves = []
    while queue:
        goal = queue.pop(0)
        if any(goal == earlier for earlier in visited):
            continue
        if len(visited) >= limit:
            raise ValueError("goal graph limit exceeded")
        visited.append(goal)
        expansions = phase165_r34_expansions(goal)
        if len(expansions) > 1:
            raise ValueError("ambiguous goal expansion")
        if not expansions:
            leaves.append(repr(goal))
        else:
            internal.append(repr(goal))
            queue.extend(expansions[0].subgoals)
    return {
        "goal": repr(root), "visited_count": len(visited),
        "derived_goal_count": len(internal), "unresolved_leaf_count": len(leaves),
        "unresolved_leaves": leaves,
    }


def audit_r34() -> dict:
    bridge, summary = build_phase165_r5_manifest_bridge()
    root = pi32_goal()
    frontier = trace_goal_frontier(root)
    citing = next((row.assertion_id for row in bridge.registry._assertions.values()
                   if row.origin.value == "fixed_statement"), None)
    if citing is None:
        raise ValueError("no registry citing assertion available")
    try:
        reconstruct_registered_goal(
            root, bridge, citing, phase165_r34_expansions,
            verified_assertion_ids=(),
        )
    except RegisteredGoalUnresolved as exc:
        status = "STRICT_BACKWARD_SEARCH_BLOCKED_ON_UNVERIFIED_LEAVES"
        reason = str(exc)
    else:
        status = "STRICT_BACKWARD_SEARCH_PROVED"
        reason = ""
    return {
        "phase": "165 R14-R34",
        **frontier,
        "source_manifest_assertions": summary.source_assertion_count,
        "existing_proof_replay_used": False,
        "strict_registry_proof_created": status == "STRICT_BACKWARD_SEARCH_PROVED",
        "strict_unresolved_reason": reason,
        "status": status,
        "full_pytest_run": False,
    }

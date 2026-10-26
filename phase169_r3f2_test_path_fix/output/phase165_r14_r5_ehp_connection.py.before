"""Phase 165 R14-R5: reuse existing EHP goal expansions without inventing evidence."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from phase165_r3_recursive_search import GoalExpansion
from phase161_r3_backward_goal_schema import expand_phase161_r3_goal


def adapt_registered_goal_expansion(
    goal: object,
    legacy_expander: Callable[[object], object | None],
) -> tuple[GoalExpansion, ...]:
    """Convert existing typed expansion contract to the common R3 contract.

    This is a structure adapter, not a citation or proof certification.
    """
    found = legacy_expander(goal)
    if found is None:
        return ()
    if type(found.goal) is not type(goal) or found.goal != goal:
        raise ValueError("EHP expansion goal mismatch")
    if not isinstance(found.subgoals, tuple):
        raise TypeError("EHP subgoals must be a tuple")
    if found.inference_rule is None:
        raise ValueError("EHP rule missing")
    return (GoalExpansion(found.inference_rule, found.subgoals),)


def expand_registered_ehp_goal(goal: object) -> tuple[GoalExpansion, ...]:
    """Common provider for existing EHP rules; no group-specific proof replay."""
    return adapt_registered_goal_expansion(goal, expand_phase161_r3_goal)


def audit_ehp_connection(goal: object, bridge) -> dict:
    """Report precisely whether a typed group goal has an expansion.

    This intentionally does not call the registered prover with a made-up
    citing assertion or approved literature ids.
    """
    options = expand_registered_ehp_goal(goal)
    matches = tuple(
        entry for entry in bridge.registry._assertions.values()
        if type(entry.content) is type(goal) and entry.content == goal
    )
    return {
        "phase": "165 R14-R5",
        "goal": repr(goal),
        "available_root_expansions": len(options),
        "registered_exact_goal_matches": len(matches),
        "registered_typed_leaf_certified": False,
        "proof_steps_created": 0,
        "legacy_proof_used": False,
        "status": (
            "ROOT_RULE_CATALOG_MISSING"
            if not options else "EHP_EXPANSIONS_AVAILABLE_NOT_CERTIFIED"
        ),
        "next_dependency": (
            "Find general, typed group-structure/iso derivation rule for this goal"
            if not options else "Verify and link all registered premise assertions"
        ),
        "full_pytest_run": False,
    }

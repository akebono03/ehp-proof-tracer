"""Phase 165 R10: diagnose fail-closed registered backward proof searches."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r2_registry_lookup import find_eligible_goal_candidates
from phase165_r3_recursive_search import (
    GoalExpansion,
    RegisteredGoalUnresolved,
    reconstruct_registered_goal,
)
from proof import ProofStep


@dataclass(frozen=True)
class GoalDiagnostic:
    status: str
    proof_step: ProofStep | None
    unresolved: tuple[str, ...]


def diagnose_registered_goal(
    goal: object,
    bridge: RegistryBridgeResult,
    citing_assertion_id: str,
    expansion_provider: Callable[[object], tuple[GoalExpansion, ...]],
    *,
    verified_assertion_ids: tuple[str, ...] = (),
) -> GoalDiagnostic:
    """Run the canonical prover, then explain its unresolved search frontier.

    The diagnostic never manufactures a premise, authorizes a citation, or
    substitutes a successful proof for the canonical prover's result.
    """
    try:
        step = reconstruct_registered_goal(
            goal, bridge, citing_assertion_id, expansion_provider,
            verified_assertion_ids=verified_assertion_ids,
        )
    except RegisteredGoalUnresolved:
        pass
    else:
        return GoalDiagnostic("PROVED", step, ())

    reasons: list[str] = []
    active: list[object] = []
    examined: list[object] = []

    def same(a: object, b: object) -> bool:
        result = type(a) is type(b) and a == b
        return type(result) is bool and result

    def explore(target: object) -> None:
        if any(same(target, item) for item in active):
            reasons.append(f"CYCLIC_OR_REVISITED_GOAL: {target!r}")
            return
        if any(same(target, item) for item in examined):
            return
        examined.append(target)
        active.append(target)
        try:
            candidates = find_eligible_goal_candidates(
                bridge, target, citing_assertion_id,
                verified_assertion_ids=verified_assertion_ids,
            )
            if any(item.proof_step is not None for item in candidates):
                return
            registered = tuple(
                entry for entry in bridge.registry._assertions.values()
                if same(entry.content, target)
            )
            if registered:
                reasons.append(f"UNVERIFIED_OR_UNLINKED_REGISTERED_GOAL: {target!r}")
            expansions = expansion_provider(target)
            if not isinstance(expansions, tuple):
                raise TypeError("expansion provider must return a tuple")
            if not expansions:
                if not registered:
                    reasons.append(f"NO_REGISTERED_GOAL_OR_INVERTIBLE_RULE: {target!r}")
                return
            for expansion in expansions:
                if not isinstance(expansion, GoalExpansion):
                    raise TypeError("invalid inference expansion")
                for subgoal in expansion.subgoals:
                    explore(subgoal)
        finally:
            active.pop()

    explore(goal)
    return GoalDiagnostic("UNRESOLVED", None, tuple(dict.fromkeys(reasons)))

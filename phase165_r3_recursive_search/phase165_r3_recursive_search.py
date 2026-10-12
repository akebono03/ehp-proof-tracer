"""Generic, fail-closed backward proof search for registered assertions.

An expansion provider supplies mathematical inference rules, never proof leaves.
All leaves must come from the verified registry lookup.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r2_registry_lookup import find_eligible_goal_candidates
from phase164_r8_proofstep_factory import derive_inference_proof_step
from proof import ProofStep, find_inference_matches_for_rule


class RegisteredGoalUnresolved(ValueError):
    """No verified and unambiguous proof exists in the available catalog."""


@dataclass(frozen=True)
class GoalExpansion:
    rule: object
    subgoals: tuple[object, ...]


def reconstruct_registered_goal(
    goal: object,
    bridge: RegistryBridgeResult,
    citing_assertion_id: str,
    expansion_provider: Callable[[object], tuple[GoalExpansion, ...]],
    *,
    verified_assertion_ids: tuple[str, ...] = (),
) -> ProofStep:
    """Resolve goal bottom-up from registered leaves and inference expansions.

    Does not construct GIVEN steps, preselect premises, use historical replays,
    or treat an unresolved citation as verified. An ambiguity is an error.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if not callable(expansion_provider):
        raise TypeError("expansion_provider must be callable")
    if not isinstance(verified_assertion_ids, tuple):
        raise TypeError("verified_assertion_ids must be a tuple")
    bridge.registry.assertion(citing_assertion_id)
    active: list[object] = []
    solved: list[tuple[object, ProofStep]] = []

    def resolve(target: object) -> ProofStep:
        for earlier, step in solved:
            if type(earlier) is type(target) and earlier == target:
                return step
        if any(type(earlier) is type(target) and earlier == target for earlier in active):
            raise RegisteredGoalUnresolved("cyclic proof dependency")
        active.append(target)
        try:
            options: list[ProofStep] = []
            candidates = find_eligible_goal_candidates(
                bridge, target, citing_assertion_id,
                verified_assertion_ids=verified_assertion_ids,
            )
            for candidate in candidates:
                if candidate.proof_step is not None:
                    options.append(candidate.proof_step)
            expansions = expansion_provider(target)
            if not isinstance(expansions, tuple):
                raise TypeError("expansion provider must return a tuple")
            for expansion in expansions:
                if not isinstance(expansion, GoalExpansion):
                    raise TypeError("invalid inference expansion")
                try:
                    premises = tuple(resolve(child) for child in expansion.subgoals)
                except RegisteredGoalUnresolved:
                    continue
                matches = tuple(
                    match for match in find_inference_matches_for_rule(
                        expansion.rule, premises,
                    )
                    if len(match.premises) == len(premises)
                    and all(a is b for a, b in zip(match.premises, premises))
                )
                for match in matches:
                    step = derive_inference_proof_step(match)
                    if type(step.conclusion) is type(target) and step.conclusion == target:
                        options.append(step)
            if len(options) != 1:
                raise RegisteredGoalUnresolved(
                    f"expected one registered derivation for {target!r}, "
                    f"found {len(options)}"
                )
            step = options[0]
            solved.append((target, step))
            return step
        finally:
            active.pop()

    return resolve(goal)

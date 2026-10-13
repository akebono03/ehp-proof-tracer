"""Shared backward search, with direct typed-reference registry lookup.

The legacy caller remains supported. New typed-reference calls require an exact
registered assertion and an exact linked ProofStep, but no independent approval.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r2_registry_lookup import find_eligible_goal_candidates
from phase164_r8_proofstep_factory import derive_inference_proof_step
from proof import ProofStep, ProofRule, find_inference_matches_for_rule
from unified_statement_registry import AssertionOrigin


class RegisteredGoalUnresolved(ValueError):
    """The requested proof has no unique derivation."""


@dataclass(frozen=True)
class GoalExpansion:
    rule: object
    subgoals: tuple[object, ...]


def _typed_reference_steps(bridge: RegistryBridgeResult, goal: object) -> tuple[ProofStep, ...]:
    """Read only exact fixed statements that have a linked given step.

    A source-only archive is not a typed statement and is not automatically
    converted; callers register concrete typed statements explicitly.
    """
    result = []
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if type(assertion.content) is not type(goal) or assertion.content != goal:
            continue
        links = tuple(x for x in bridge.proof_links if x.assertion_id == assertion.assertion_id)
        if len(links) != 1 or links[0].step is None:
            continue
        step = links[0].step
        if (not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN
                or type(step.conclusion) is not type(goal) or step.conclusion != goal):
            raise ValueError("typed Reference proof link is inconsistent")
        result.append(step)
    return tuple(result)


def reconstruct_registered_goal(
    goal: object,
    bridge: RegistryBridgeResult,
    citing_assertion_id: str,
    expansion_provider: Callable[[object], tuple[GoalExpansion, ...]],
    *,
    verified_assertion_ids: tuple[str, ...] = (),
    lookup_mode: str = "legacy",
) -> ProofStep:
    """Derive recursively using typed References or legacy candidates.

    lookup_mode='typed_reference' does not impose a separate citation-approval
    gate. It still requires exact typed equality and provenance-linked steps.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if not callable(expansion_provider):
        raise TypeError("expansion_provider must be callable")
    if not isinstance(verified_assertion_ids, tuple):
        raise TypeError("verified_assertion_ids must be a tuple")
    if lookup_mode not in ("legacy", "typed_reference"):
        raise ValueError("unknown lookup mode")
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
            if lookup_mode == "typed_reference":
                options = list(_typed_reference_steps(bridge, target))
            else:
                candidates = find_eligible_goal_candidates(
                    bridge, target, citing_assertion_id,
                    verified_assertion_ids=verified_assertion_ids,
                )
                options = [x.proof_step for x in candidates if x.proof_step is not None]
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
                    match for match in find_inference_matches_for_rule(expansion.rule, premises)
                    if len(match.premises) == len(premises)
                    and all(a is b for a, b in zip(match.premises, premises))
                )
                for match in matches:
                    step = derive_inference_proof_step(match)
                    if type(step.conclusion) is type(target) and step.conclusion == target:
                        options.append(step)
            if len(options) != 1:
                raise RegisteredGoalUnresolved(
                    f"expected one registered derivation for {target!r}, found {len(options)}"
                )
            step = options[0]
            solved.append((target, step))
            return step
        finally:
            active.pop()

    return resolve(goal)

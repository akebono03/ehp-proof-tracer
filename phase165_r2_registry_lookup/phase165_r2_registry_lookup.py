"""Phase 165 R2: shared, fail-closed registry lookup for proof goals.

This module does not construct proof facts or infer missing proof steps.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase164_r2_citation_eligibility import assess_phase164_r2_citation
from unified_statement_registry import AssertionEntry, AssertionOrigin


@dataclass(frozen=True)
class RegisteredGoalCandidate:
    assertion: AssertionEntry
    proof_step: object | None


def find_eligible_goal_candidates(
    bridge: RegistryBridgeResult,
    goal: object,
    citing_assertion_id: str,
    *,
    verified_assertion_ids: tuple[str, ...] = (),
) -> tuple[RegisteredGoalCandidate, ...]:
    """Find eligible fixed assertions matching an exact typed goal.

    Eligibility always uses the established Phase 164 citation policy.
    No source-archive, internal-proof or unreviewed claim is promoted.
    Existing proof links are not assumed to exist or to be independently valid.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if not isinstance(citing_assertion_id, str) or not citing_assertion_id.strip():
        raise ValueError("citing_assertion_id must be nonempty")
    if not isinstance(verified_assertion_ids, tuple):
        raise TypeError("verified_assertion_ids must be a tuple")
    bridge.registry.assertion(citing_assertion_id)
    candidates: list[RegisteredGoalCandidate] = []
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if type(assertion.content) is not type(goal):
            continue
        same = assertion.content == goal
        if type(same) is not bool or not same:
            continue
        decision = assess_phase164_r2_citation(
            bridge,
            assertion.assertion_id,
            citing_assertion_id,
            verified_assertion_ids=verified_assertion_ids,
        )
        if not decision.usable:
            continue
        links = tuple(
            link for link in bridge.proof_links
            if link.assertion_id == assertion.assertion_id
        )
        if len(links) > 1:
            raise ValueError("ambiguous ProofStepLink")
        proof_step = links[0].step if links else None
        if proof_step is not None:
            if type(proof_step.conclusion) is not type(goal):
                raise ValueError("proof link conclusion type mismatch")
            match = proof_step.conclusion == goal
            if type(match) is not bool or not match:
                raise ValueError("proof link conclusion mismatch")
        candidates.append(RegisteredGoalCandidate(assertion, proof_step))
    return tuple(candidates)


def require_unique_registered_proof_step(
    bridge: RegistryBridgeResult,
    goal: object,
    citing_assertion_id: str,
    *,
    verified_assertion_ids: tuple[str, ...] = (),
) -> object:
    """Return an independently linked proof step, or fail closed.

    The registry may hold an eligible assertion with no proof implementation.
    In that case the caller must not fabricate a GIVEN step.
    """
    candidates = find_eligible_goal_candidates(
        bridge, goal, citing_assertion_id,
        verified_assertion_ids=verified_assertion_ids,
    )
    steps = tuple(item.proof_step for item in candidates if item.proof_step is not None)
    if len(steps) != 1:
        raise ValueError(
            "registered goal has no unique verified ProofStep; "
            "proof search must not invent a premise"
        )
    return steps[0]

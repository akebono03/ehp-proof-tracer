"""R12-R18: extract only complete proof roots and inspect generator witnesses.

Does not create literature facts or certify missing generator images.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r52_partial_proof import ProofSearchStatus
from proof import ProofStep, ProofRule


@dataclass(frozen=True)
class EvidenceResult:
    status: str
    proof: ProofStep | None
    reason: str | None


def extract_completed_root(result: object, expected_goal: object) -> EvidenceResult:
    """Select the unique root from a completed canonical PartialProofResult."""
    if getattr(result, "status", None) is not ProofSearchStatus.COMPLETE:
        return EvidenceResult("UNRESOLVED", None, "canonical search is not complete")
    if getattr(result, "conclusion", None) != expected_goal:
        return EvidenceResult("UNRESOLVED", None, "completed conclusion differs from goal")
    if getattr(result, "open_goals", ()):
        return EvidenceResult("UNRESOLVED", None, "open goals remain")
    roots = tuple(
        step for step in getattr(result, "proven_steps", ())
        if isinstance(step, ProofStep)
        and type(step.conclusion) is type(expected_goal)
        and step.conclusion == expected_goal
    )
    if len(roots) != 1:
        return EvidenceResult("UNRESOLVED", None, "expected exactly one proved root")
    if roots[0].rule is not ProofRule.INFERENCE:
        return EvidenceResult("UNRESOLVED", None, "group root must be an inference")
    return EvidenceResult("PROVEN_ROOT", roots[0], None)


def find_screened_generator_witness(bridge: object, goal: object) -> EvidenceResult:
    """Read an exact fixed-source generator witness, rejecting unknown origin."""
    from unified_statement_registry import AssertionOrigin
    matches = []
    for link in bridge.proof_links:
        step = link.step
        if step is None or not isinstance(step, ProofStep):
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if (assertion.origin is AssertionOrigin.FIXED_STATEMENT
                and step.rule is ProofRule.GIVEN
                and step.conclusion == assertion.content
                and type(step.conclusion) is type(goal)
                and step.conclusion == goal):
            matches.append(step)
    if len(matches) != 1:
        return EvidenceResult("UNRESOLVED", None, "no unique eligible typed generator witness")
    return EvidenceResult("CITED_WITNESS", matches[0], None)

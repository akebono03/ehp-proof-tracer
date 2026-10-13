"""R14-R16: canonical foundational suspension identity with provenance boundary."""
from __future__ import annotations

from dataclasses import dataclass

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from proof import FoundationalReferenceIdentity
from phase165_r14_r14_diagonal_and_prop42 import (
    GeneratorSuspension, diagonal_suspension_subgoals, review_prop42_scope,
)
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge


FOUNDATIONAL_SUSPENSION_IDENTITY = FoundationalReferenceIdentity(
    key="foundational:suspension-identity",
    label="Suspension of the identity map (well-known foundational property)",
)


@dataclass(frozen=True)
class FoundationalClaim:
    statement: GeneratorSuspension
    reference: FoundationalReferenceIdentity
    justification: str
    literature_assertion_id: str | None = None
    independently_reviewed: bool = False
    proof_eligible: bool = False


def instantiate_foundational_identity_suspension(n: int) -> FoundationalClaim:
    """Construct E(iota_n)=iota_(n+1), n>=1, not a Toda citation."""
    if type(n) is not int or n < 1:
        raise ValueError("n must be a positive integer")
    suspension = TodaSuspensionMap(TodaPrimaryGroup(n,n),TodaPrimaryGroup(n+1,n+1))
    goals = diagonal_suspension_subgoals(suspension)
    if goals is None or not isinstance(goals[2], GeneratorSuspension):
        raise ValueError("diagonal suspension statement unavailable")
    return FoundationalClaim(
        statement=goals[2],
        reference=FOUNDATIONAL_SUSPENSION_IDENTITY,
        justification=(
            "Under S(S^n) = S^(n+1), the reduced suspension of "
            "id_(S^n) is id_(S^(n+1)); hence E(iota_n)=iota_(n+1)."
        ),
    )


def bind_foundational_diagonal_obligations(n: int) -> tuple[object, ...]:
    """Return all three genuine obligations; do not manufacture leaves."""
    statement = instantiate_foundational_identity_suspension(n).statement
    goals = diagonal_suspension_subgoals(statement.map)
    if goals is None or goals[2] != statement:
        raise ValueError("generator correspondence mismatch")
    return goals


def audit_r16(bridge=None) -> dict:
    if bridge is None:
        bridge, _ = build_phase165_r5_manifest_bridge()
    before = (len(bridge.registry._assertions), len(bridge.proof_links))
    claim = instantiate_foundational_identity_suspension(1)
    reviews = review_prop42_scope(bridge)
    after = (len(bridge.registry._assertions), len(bridge.proof_links))
    if before != after:
        raise ValueError("read-only audit modified the registry")
    return {
        "phase": "165 R14-R16",
        "foundational_claim": repr(claim.statement),
        "foundational_reference": claim.reference.key,
        "foundational_justification": claim.justification,
        "classification": "WELL_KNOWN_FOUNDATIONAL_NOT_TODA_LITERATURE",
        "foundational_claim_formulated": True,
        "foundational_claim_independently_reviewed": False,
        "foundational_claim_proof_eligible": False,
        "diagonal_obligation_count": len(bind_foundational_diagonal_obligations(1)),
        "prop42_candidate_count": len(reviews),
        "prop42_candidates": [
            {"assertion_id": r["assertion_id"],
             "locator": r["locator"],
             "source_text": r["source_text"],
             "application_verified": False}
            for r in reviews
        ],
        "prop42_clause_selected": False,
        "prop42_proof_eligible": False,
        "new_proof_steps": 0,
        "status": "FOUNDATIONAL_IDENTITY_TYPED_PROP42_STILL_REQUIRES_REVIEW",
        "full_pytest_run": False,
    }

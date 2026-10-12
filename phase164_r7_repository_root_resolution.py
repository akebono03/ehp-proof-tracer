"""Phase 164 R7-R4: shared internal proof-root resolution for all repository queries.

The bridge records existing internal proof roots, not verified literature.
This module neither constructs nor authorizes mathematical ProofSteps.
"""
from types import SimpleNamespace

from phase163_r4_registry_bridge import build_registry_bridge
from phase164_r7_statement_resolution import resolve_registered_statement
from proof_repository import ProofRepository
from unified_statement_registry import AssertionOrigin


def validate_repository_internal_proof_roots(
    repository: ProofRepository,
) -> ProofRepository:
    """Fail closed on inconsistent registered root steps, preserving identity."""
    if not isinstance(repository, ProofRepository):
        raise TypeError("repository must be a ProofRepository")

    bridge = build_registry_bridge(
        components_by_reference={},
        theorem_facts=SimpleNamespace(entries=()),
        proof_repository=repository,
    )
    for entry in repository.entries():
        resolved = resolve_registered_statement(
            bridge,
            f"repository:{entry.key}:conclusion",
            proof_repository=repository,
            expected_conclusion=entry.step.conclusion,
        )
        if resolved.assertion.origin is not AssertionOrigin.PROOF_INTERNAL:
            raise ValueError("repository root must remain proof-internal")
        if resolved.proof_link is None or resolved.proof_link.step is not entry.step:
            raise ValueError("repository root ProofStep identity mismatch")
    return repository

"""Phase 164 R7: read-only, fail-closed statement resolution.

Registry identities are canonical; a proof repository is only a storage backend.
This module neither creates ProofSteps nor changes citation eligibility.
"""
from dataclasses import dataclass
from typing import Any

from phase163_r4_registry_bridge import MigrationStatus, RegistryBridgeResult
from phase164_r2_citation_eligibility import assess_phase164_r2_citation
from unified_statement_registry import AssertionEntry, AssertionOrigin, LiteratureEntry, ProofStepLink


@dataclass(frozen=True)
class ResolvedStatement:
    assertion: AssertionEntry
    reference: LiteratureEntry
    migration_status: MigrationStatus
    proof_link: ProofStepLink | None


def resolve_registered_statement(
    bridge: RegistryBridgeResult,
    assertion_id: str,
    *,
    proof_repository: Any = None,
    expected_conclusion: Any = None,
    citing_assertion_id: str | None = None,
    verified_assertion_ids: tuple[str, ...] = (),
) -> ResolvedStatement:
    """Resolve one assertion without treating registration as proof verification.

    When citing_assertion_id is specified, require the existing R2 citation
    policy to allow the reference. A proof link is checked against the actual
    repository entry if one is supplied. No arbitrary link is proof eligible.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if not isinstance(assertion_id, str) or not assertion_id.strip():
        raise ValueError("assertion_id must be nonempty")
    assertion = bridge.registry.assertion(assertion_id)
    reference = bridge.registry.reference(assertion.reference_id)
    records = tuple(record for record in bridge.records if record.assertion_id == assertion_id)
    if len(records) != 1:
        raise ValueError("migration record missing or ambiguous")
    status = records[0].status
    if status is not MigrationStatus.STRUCTURED:
        raise ValueError(f"assertion not structured: {status.value}")
    if assertion.origin is AssertionOrigin.SOURCE_ARCHIVE:
        raise ValueError("source_archive_not_verified")

    if expected_conclusion is not None:
        if type(assertion.content) is not type(expected_conclusion):
            raise ValueError("registered conclusion type mismatch")
        equality = assertion.content == expected_conclusion
        if type(equality) is not bool or not equality:
            raise ValueError("registered conclusion mismatch")

    links = tuple(link for link in bridge.proof_links if link.assertion_id == assertion_id)
    if len(links) > 1:
        raise ValueError("ambiguous ProofStepLink")
    link = links[0] if links else None
    if link is not None:
        if assertion.origin is not AssertionOrigin.PROOF_INTERNAL:
            raise ValueError("fixed literature cannot inherit internal proof link")
        step = link.step
        if proof_repository is not None and link.repository_key is not None:
            repository_step = proof_repository.get(link.repository_key).step
            if step is not None and step is not repository_step:
                raise ValueError("proof link/repository identity mismatch")
            step = repository_step
        if step is not None:
            if type(step.conclusion) is not type(assertion.content):
                raise ValueError("proof link conclusion type mismatch")
            equality = step.conclusion == assertion.content
            if type(equality) is not bool or not equality:
                raise ValueError("proof link conclusion mismatch")

    if citing_assertion_id is not None:
        eligibility = assess_phase164_r2_citation(
            bridge, assertion_id, citing_assertion_id,
            verified_assertion_ids=verified_assertion_ids,
        )
        if not eligibility.usable:
            raise ValueError(
                f"citation not eligible: {assertion_id}: "
                f"{eligibility.status.value}/{eligibility.reason}"
            )
    return ResolvedStatement(assertion, reference, status, link)

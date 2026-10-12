"""Phase 164 R2: fail-closed citation eligibility, without proof search integration.

An explicit verified_assertion_ids allowlist is a caller-supplied review record,
not a mathematical verification performed by this module. No production entry
is automatically approved. An ALLOWED outcome requires *all* safeguards.
"""
from dataclasses import dataclass
from enum import Enum

from phase163_r3_registry_validation import (
    CitationDecision,
    assess_citation,
    audit_dependencies,
)
from phase163_r4_registry_bridge import MigrationStatus, RegistryBridgeResult
from unified_statement_registry import AssertionOrigin


class EligibilityStatus(str, Enum):
    ALLOWED = "allowed"
    DENIED = "denied"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class EligibilityResult:
    status: EligibilityStatus
    reason: str
    cited_assertion_id: str

    @property
    def usable(self) -> bool:
        return self.status is EligibilityStatus.ALLOWED


def assess_phase164_r2_citation(
    bridge: RegistryBridgeResult,
    cited_assertion_id: str,
    citing_assertion_id: str,
    *,
    verified_assertion_ids: tuple[str, ...] = (),
) -> EligibilityResult:
    """Assess an external citation; UNKNOWN or DENIED must never be used.

    `verified_assertion_ids` MUST be independently reviewed and must not be
    populated by listing the registry or the archival manifest. Even an
    approved ID cannot bypass structural, dependency, or ordering checks.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if not isinstance(cited_assertion_id, str) or not cited_assertion_id.strip():
        raise ValueError("cited_assertion_id must be nonempty")
    if not isinstance(citing_assertion_id, str) or not citing_assertion_id.strip():
        raise ValueError("citing_assertion_id must be nonempty")
    if not isinstance(verified_assertion_ids, tuple) or any(
        not isinstance(identifier, str) or not identifier.strip()
        for identifier in verified_assertion_ids
    ):
        raise TypeError("verified_assertion_ids must be a tuple of nonempty strings")

    registry = bridge.registry
    cited = registry.assertion(cited_assertion_id)
    registry.assertion(citing_assertion_id)

    def outcome(status: EligibilityStatus, reason: str) -> EligibilityResult:
        return EligibilityResult(status, reason, cited_assertion_id)

    if cited_assertion_id == citing_assertion_id:
        return outcome(EligibilityStatus.DENIED, "self_citation")
    if cited.origin is AssertionOrigin.SOURCE_ARCHIVE:
        return outcome(EligibilityStatus.DENIED, "source_archive_not_verified")
    if cited.origin is AssertionOrigin.PROOF_INTERNAL:
        return outcome(EligibilityStatus.DENIED, "proof_internal_not_external_reference")
    if cited.origin is not AssertionOrigin.FIXED_STATEMENT:
        return outcome(EligibilityStatus.UNKNOWN, "unrecognized_origin")

    record_statuses = tuple(
        record.status for record in bridge.records
        if record.assertion_id == cited_assertion_id
    )
    if len(record_statuses) != 1:
        return outcome(EligibilityStatus.UNKNOWN, "migration_record_missing_or_ambiguous")
    if record_statuses[0] is MigrationStatus.METADATA_ONLY:
        return outcome(EligibilityStatus.DENIED, "metadata_only")
    if record_statuses[0] is not MigrationStatus.STRUCTURED:
        return outcome(EligibilityStatus.UNKNOWN, "unresolved_structured_statement")

    dependency_audit = audit_dependencies(registry)
    if not dependency_audit.valid:
        return outcome(EligibilityStatus.UNKNOWN, "dependency_graph_unverified")
    if citing_assertion_id in cited.dependencies:
        return outcome(EligibilityStatus.DENIED, "depends_on_citing_assertion")
    if cited_assertion_id not in verified_assertion_ids:
        return outcome(EligibilityStatus.UNKNOWN, "independent_verification_not_recorded")
    for dependency_id in cited.dependencies:
        dependency = registry.assertion(dependency_id)
        if dependency.origin is not AssertionOrigin.FIXED_STATEMENT:
            return outcome(EligibilityStatus.UNKNOWN, "dependency_not_fixed")
        if dependency_id not in verified_assertion_ids:
            return outcome(EligibilityStatus.UNKNOWN, "dependency_not_verified")
        dependency_records = tuple(
            record.status for record in bridge.records
            if record.assertion_id == dependency_id
        )
        if dependency_records != (MigrationStatus.STRUCTURED,):
            return outcome(EligibilityStatus.UNKNOWN, "dependency_not_structured")

    prior = assess_citation(registry, cited_assertion_id, citing_assertion_id)
    if prior.decision is CitationDecision.DENIED:
        return outcome(EligibilityStatus.DENIED, prior.reason)
    if prior.decision is CitationDecision.UNKNOWN:
        return outcome(EligibilityStatus.UNKNOWN, prior.reason)
    return outcome(EligibilityStatus.ALLOWED, "reviewed_structured_available_citation")

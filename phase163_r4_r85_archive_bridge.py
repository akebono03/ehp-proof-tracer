"""Phase 163 R4-R85: explicit archival Bridge integration, never proof-search eligible."""
from __future__ import annotations

from pathlib import Path

from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
    build_registry_bridge,
)
from phase163_source_archive_registry import (
    CATALOG_PATH,
    build_registry_with_source_archive,
)
from unified_statement_registry import AssertionOrigin


def build_registry_bridge_with_source_archive(
    catalog_path: Path = CATALOG_PATH,
) -> RegistryBridgeResult:
    """Build one Bridge and explicitly attach source-only metadata records.

    No ProofStepLink is created for source archive assertions. Existing
    build_registry_bridge() semantics and proof links remain unchanged.
    """
    base = build_registry_bridge()
    registry, summary = build_registry_with_source_archive(
        catalog_path, bridge=base
    )
    identities = summary["source_text_assertion_ids"]
    records = []
    for assertion_id in identities:
        assertion = registry.assertion(assertion_id)
        if (assertion.origin is not AssertionOrigin.SOURCE_ARCHIVE
                or assertion.available_after_position is not None
                or assertion.content.get("proof_eligible") is not False
                or assertion.content.get("mathematics_verified") is not False):
            raise ValueError("archival assertion was promoted to a proof premise")
        records.append(MigrationRecord(
            source="source_archive",
            source_key=assertion_id,
            assertion_id=assertion_id,
            status=MigrationStatus.METADATA_ONLY,
            detail="TeX source transcription; not a verified mathematical premise",
        ))
    if len(records) != 8 or len(set(identities)) != 8:
        raise ValueError("unexpected archival assertion count")
    return RegistryBridgeResult(
        registry=registry,
        records=base.records + tuple(records),
        proof_links=base.proof_links,
    )

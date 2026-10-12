"""Connect Phase 163 source-order archive to the R3 registry bridge.

Archive entries are explicitly NOT eligible proof premises. This preserves
source ordering without fabricating a completion position or typed ProofStep.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
    build_registry_bridge,
)
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ReferenceKind,
    UnifiedStatementRegistry,
)

DEFAULT_MANIFEST = Path(__file__).resolve().with_name(
    "phase163_r4_r94_output"
).joinpath("manifest.json")


@dataclass(frozen=True)
class ManifestBridgeSummary:
    source_reference_count: int
    source_assertion_count: int
    existing_assertion_count: int
    newly_eligible_count: int
    proof_link_count: int


def build_phase165_r5_manifest_bridge(
    manifest_path: Path = DEFAULT_MANIFEST,
    *,
    base_bridge: RegistryBridgeResult | None = None,
) -> tuple[RegistryBridgeResult, ManifestBridgeSummary]:
    """Import source identity/order as non-citable archive records only.

    Existing structured assertions and proof links keep their original
    identities. The manifest never supplies typed semantics, completion
    positions, verification status, or new ProofSteps.
    """
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8-sig"))
    if (manifest.get("phase") != "163 R4-R94"
            or manifest.get("mode") != "ORDERED_SOURCE_ONLY_MANIFEST"
            or manifest.get("publication_order_scope") != "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION"
            or manifest.get("original_edition_verified") is not False
            or manifest.get("mathematical_semantics_verified_count") != 0
            or manifest.get("proof_eligible_count") != 0
            or manifest.get("proof_search_connected") is not False):
        raise ValueError("manifest provenance/eligibility contract invalid")
    rows = manifest.get("assertions")
    if (not isinstance(rows, list)
            or len(rows) != manifest.get("assertion_count")
            or len(rows) != 117):
        raise ValueError("source assertion count mismatch")
    refs = {}
    previous = None
    seen_ids = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("invalid archive assertion")
        source_id = row.get("statement_id")
        ref_id = row.get("reference_id")
        location = row.get("locator")
        text = row.get("source_text")
        sha = row.get("source_sha256")
        pos = row.get("publication_position")
        ch = row.get("chapter")
        if (not all(isinstance(x, str) and x for x in (source_id, ref_id, location, text, sha))
                or source_id in seen_ids
                or isinstance(pos, bool) or not isinstance(pos, int) or pos <= 0
                or isinstance(ch, bool) or not isinstance(ch, int) or not 1 <= ch <= 5
                or hashlib.sha256(text.encode("utf-8")).hexdigest() != sha):
            raise ValueError("invalid source identity, position or checksum")
        key = (ch, pos)
        if previous is not None and key < previous:
            raise ValueError("source order reversed")
        previous = key
        seen_ids.add(source_id)
        if ref_id in refs and refs[ref_id] != location:
            raise ValueError("reference locator identity mismatch")
        refs[ref_id] = location
    if len(refs) != manifest.get("reference_count") or len(refs) != 108:
        raise ValueError("source reference count mismatch")

    source = build_registry_bridge() if base_bridge is None else base_bridge
    if not isinstance(source, RegistryBridgeResult):
        raise TypeError("base_bridge must be RegistryBridgeResult")
    registry = UnifiedStatementRegistry()
    for entry in source.registry._references.values():
        registry.add_reference(entry)
    for entry in source.registry._assertions.values():
        registry.add_assertion(entry)
    records = list(source.records)
    for ref_id, locator in refs.items():
        representative = next(item for item in rows if item["reference_id"] == ref_id)
        archive_ref_id = "phase163:archive:" + ref_id
        try:
            kind = ReferenceKind(representative["kind"])
        except (KeyError, ValueError) as exc:
            raise ValueError("unsupported reference kind") from exc
        registry.add_reference(LiteratureEntry(
            reference_id=archive_ref_id,
            kind=kind,
            locator=locator,
            source_id="Toda translated TeX; not original edition verified",
            publication_position=representative["publication_position"],
        ))
    for row in rows:
        source_id = row["statement_id"]
        assertion_id = "phase163:archive:" + source_id
        registry.add_assertion(AssertionEntry(
            assertion_id=assertion_id,
            reference_id="phase163:archive:" + row["reference_id"],
            kind=AssertionKind.STATEMENT,
            content={
                "source_statement_id": source_id,
                "source_text": row["source_text"],
                "source_sha256": row["source_sha256"],
                "source_chapter": row["chapter"],
                "source_position": row["publication_position"],
                "proof_eligible": False,
            },
            origin=AssertionOrigin.SOURCE_ARCHIVE,
            component_position=row.get("component_position"),
            available_after_position=None,
        ))
        records.append(MigrationRecord(
            source="phase163_r4_r94_source_manifest",
            source_key=source_id,
            assertion_id=assertion_id,
            status=MigrationStatus.METADATA_ONLY,
            detail="Source order only; mathematics and availability unverified",
        ))
    bridge = RegistryBridgeResult(registry, tuple(records), source.proof_links)
    return bridge, ManifestBridgeSummary(
        source_reference_count=len(refs),
        source_assertion_count=len(rows),
        existing_assertion_count=len(source.registry._assertions),
        newly_eligible_count=0,
        proof_link_count=len(source.proof_links),
    )

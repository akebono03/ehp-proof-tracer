"""Phase 166 R3-B: connect existing Phase 163 publication order to typed registry entries.

This module reuses the immutable Phase 163 R4-R94 manifest.  It does not
recompute source order, parse TeX, authorize citations, or alter proof order.
Only exact literature reference IDs are joined.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import json
from pathlib import Path

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r5_manifest_bridge import DEFAULT_MANIFEST
from unified_statement_registry import UnifiedStatementRegistry


@dataclass(frozen=True)
class PublicationOrderBinding:
    reference_id: str
    publication_position: int
    typed_assertion_ids: tuple[str, ...]
    source_statement_ids: tuple[str, ...]


@dataclass(frozen=True)
class PublicationOrderBindingSummary:
    manifest_reference_count: int
    manifest_assertion_count: int
    typed_reference_count: int
    connected_reference_count: int
    connected_assertion_count: int
    unchanged_reference_count: int
    proof_link_count: int
    bindings: tuple[PublicationOrderBinding, ...]


def _load_manifest_reference_order(manifest_path: Path) -> tuple[dict[str, int], dict[str, tuple[dict, ...]], dict]:
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8-sig"))
    if (manifest.get("phase") != "163 R4-R94"
            or manifest.get("mode") != "ORDERED_SOURCE_ONLY_MANIFEST"
            or manifest.get("reference_count") != 108
            or manifest.get("assertion_count") != 117
            or manifest.get("publication_order_scope") != "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION"
            or manifest.get("proof_search_connected") is not False):
        raise ValueError("Phase 163 publication-order manifest contract changed")

    rows = manifest.get("assertions")
    if not isinstance(rows, list) or len(rows) != 117:
        raise ValueError("Phase 163 manifest assertion count changed")

    positions: dict[str, int] = {}
    rows_by_reference: dict[str, list[dict]] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("invalid manifest assertion row")
        reference_id = row.get("reference_id")
        publication_position = row.get("publication_position")
        statement_id = row.get("statement_id")
        component_position = row.get("component_position")
        if (not isinstance(reference_id, str) or not reference_id
                or not isinstance(statement_id, str) or not statement_id
                or isinstance(publication_position, bool)
                or not isinstance(publication_position, int)
                or publication_position <= 0
                or (component_position is not None
                    and (isinstance(component_position, bool)
                         or not isinstance(component_position, int)
                         or component_position <= 0))):
            raise ValueError("invalid manifest reference/order row")
        previous = positions.setdefault(reference_id, publication_position)
        if previous != publication_position:
            raise ValueError("one literature reference has multiple publication positions")
        rows_by_reference.setdefault(reference_id, []).append(row)

    if len(positions) != 108 or sorted(positions.values()) != list(range(100, 10900, 100)):
        raise ValueError("Phase 163 reference publication order changed")

    frozen_rows = {
        reference_id: tuple(sorted(items, key=lambda item: (
            item.get("component_position") or 0,
            item["statement_id"],
        )))
        for reference_id, items in rows_by_reference.items()
    }
    return positions, frozen_rows, manifest


def connect_phase163_publication_order(
    bridge: RegistryBridgeResult,
    manifest_path: Path = DEFAULT_MANIFEST,
) -> tuple[RegistryBridgeResult, PublicationOrderBindingSummary]:
    """Attach existing publication positions to exact-ID typed references.

    No locator fallback is allowed.  Assertion component positions,
    dependencies, contents, origins, migration records, and proof links are
    preserved byte-for-byte/by identity through the copied registry snapshot.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")

    positions, rows_by_reference, manifest = _load_manifest_reference_order(manifest_path)
    registry = UnifiedStatementRegistry()
    connected_reference_ids: set[str] = set()

    for reference in bridge.registry._references.values():
        position = positions.get(reference.reference_id)
        if position is None:
            registry.add_reference(reference)
            continue
        if (reference.publication_position is not None
                and reference.publication_position != position):
            raise ValueError(
                f"typed publication position conflicts with Phase 163 manifest: {reference.reference_id}"
            )
        registry.add_reference(replace(reference, publication_position=position))
        connected_reference_ids.add(reference.reference_id)

    for assertion in bridge.registry._assertions.values():
        registry.add_assertion(assertion)

    bindings = []
    connected_assertion_count = 0
    for reference_id in sorted(connected_reference_ids, key=lambda item: positions[item]):
        typed_assertions = registry.assertions_for(reference_id)
        connected_assertion_count += len(typed_assertions)
        source_rows = rows_by_reference[reference_id]
        bindings.append(PublicationOrderBinding(
            reference_id=reference_id,
            publication_position=positions[reference_id],
            typed_assertion_ids=tuple(item.assertion_id for item in typed_assertions),
            source_statement_ids=tuple(item["statement_id"] for item in source_rows),
        ))

    result = RegistryBridgeResult(registry, bridge.records, bridge.proof_links)
    summary = PublicationOrderBindingSummary(
        manifest_reference_count=manifest["reference_count"],
        manifest_assertion_count=manifest["assertion_count"],
        typed_reference_count=len(bridge.registry._references),
        connected_reference_count=len(connected_reference_ids),
        connected_assertion_count=connected_assertion_count,
        unchanged_reference_count=len(bridge.registry._references) - len(connected_reference_ids),
        proof_link_count=len(bridge.proof_links),
        bindings=tuple(bindings),
    )
    return result, summary

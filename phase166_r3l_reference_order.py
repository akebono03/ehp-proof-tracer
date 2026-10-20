"""Phase 166 R3-L: connect every registered reference to existing source order.

Only immutable manifest IDs, exact source statement IDs and explicitly reviewed
reference-ID aliases are used. An unresolvable source is reported, never guessed.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r5_manifest_bridge import DEFAULT_MANIFEST
from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import (
    _load_manifest_reference_order,
)
from unified_statement_registry import UnifiedStatementRegistry


# Reviewed reference identities, not locator/string matching. The manifest
# remains the sole source of numeric positions.
REVIEWED_REFERENCE_ALIASES: dict[str, str] = {
    "adopted:ref:1": "toda:(5.1)",
    "adopted:ref:2": "toda:(5.1)",
    "adopted:ref:4": "toda:(5.1)",
    "adopted:ref:5": "toda:Proposition 5.1",
    "adopted:ref:6": "toda:(5.1)",
    "adopted:toda:adopted:prop5.1:finite_dimensional": "toda:Proposition 5.1",
    "adopted:toda51:diagonal": "toda:(5.1)",
    "adopted:reference:toda51:below_diagonal_zero": "toda:(5.1)",
    "typed_literature:toda:tex:ch4:0006": "toda:(4.5)",
    "typed_literature:toda:tex:ch4:0010": "toda:Proposition 4.4",
    "typed_literature:toda:tex:ch5:0003": "toda:(5.2)",
}


@dataclass(frozen=True)
class ReferenceOrderReport:
    total: int
    connected: int
    previously_connected: int
    unresolved: tuple[str, ...]
    aliases_used: tuple[tuple[str, str], ...]


def connect_all_reference_orders(
    bridge: RegistryBridgeResult,
    manifest_path: Path = DEFAULT_MANIFEST,
) -> tuple[RegistryBridgeResult, ReferenceOrderReport]:
    """Bind all reference entries; preserve assertions, proof links and identities.

    Unknown or ambiguous identifiers are left unset and listed in the report.
    No eligibility, inference or proof-completion decision is made here.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    positions, rows_by_reference, _manifest = _load_manifest_reference_order(manifest_path)
    source_to_reference: dict[str, str] = {}
    ambiguous: set[str] = set()
    for ref_id, rows in rows_by_reference.items():
        for row in rows:
            source_id = row["statement_id"]
            if source_id in source_to_reference and source_to_reference[source_id] != ref_id:
                ambiguous.add(source_id)
            else:
                source_to_reference[source_id] = ref_id

    registry = UnifiedStatementRegistry()
    unresolved: list[str] = []
    used: list[tuple[str, str]] = []
    connected = 0
    previously = 0
    for ref in bridge.registry._references.values():
        original_id = ref.reference_id
        # Shared-bridge namespaces are purely mechanical; remove one prefix.
        suffix = original_id.split(":", 2)[2] if original_id.startswith("shared:") and len(original_id.split(":", 2)) == 3 else original_id
        canonical = None
        if suffix in positions:
            canonical = suffix
        elif suffix in REVIEWED_REFERENCE_ALIASES:
            canonical = REVIEWED_REFERENCE_ALIASES[suffix]
            used.append((original_id, canonical))
        elif ref.source_id and ref.source_id not in ambiguous:
            canonical = source_to_reference.get(ref.source_id)
        if canonical is not None and canonical not in positions:
            raise ValueError("reviewed mapping missing from manifest: " + canonical)
        if canonical is None:
            if ref.publication_position is None:
                unresolved.append(original_id)
            else:
                previously += 1
            registry.add_reference(ref)
            continue
        expected = positions[canonical]
        if ref.publication_position is not None and ref.publication_position != expected:
            raise ValueError("conflicting source order: " + original_id)
        registry.add_reference(replace(ref, publication_position=expected))
        connected += 1

    for assertion in bridge.registry._assertions.values():
        registry.add_assertion(assertion)
    return RegistryBridgeResult(registry, bridge.records, bridge.proof_links), ReferenceOrderReport(
        total=len(bridge.registry._references),
        connected=connected,
        previously_connected=previously,
        unresolved=tuple(unresolved),
        aliases_used=tuple(used),
    )

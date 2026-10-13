"""Attach all six (5.1) clauses to its existing archival reference."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from phase163_r4_registry_bridge import RegistryBridgeResult, MigrationRecord, MigrationStatus
from phase165_r14_r21_toda51_completion import (
    CLAUSE_KEYS, complete_toda51_source, diagonal_specializations,
)
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, UnifiedStatementRegistry,
)


@dataclass(frozen=True)
class Toda51Integration:
    bridge: RegistryBridgeResult
    reference_id: str
    component_ids: tuple[str, ...]
    original_reference_count: int
    original_assertion_count: int


def integrate_toda51_into_existing_reference(
    bridge: RegistryBridgeResult, tex: str,
) -> Toda51Integration:
    """Copy the registry, retaining the existing (5.1) reference identity.

    Six components remain SOURCE_ARCHIVE. Two n=1,2 instances are recorded
    as typed specializations on the diagonal component, not as proof facts.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    completed = complete_toda51_source(tex)
    matches = tuple(
        ref for ref in bridge.registry._references.values()
        if ref.locator == "(5.1)" and ref.reference_id.startswith("phase163:archive:")
    )
    if len(matches) != 1:
        raise ValueError("exactly one existing archival (5.1) reference required")
    ref_id = matches[0].reference_id
    old = bridge.registry
    registry = UnifiedStatementRegistry()
    for ref in old._references.values():
        registry.add_reference(ref)
    for assertion in old._assertions.values():
        registry.add_assertion(assertion)
    records = list(bridge.records)
    ids = tuple("phase165:r14r22:toda51:" + key for key in CLAUSE_KEYS)
    if any(aid in registry._assertions for aid in ids):
        raise ValueError("six components already registered")
    typed_diagonal = diagonal_specializations(completed)
    for i, (aid, clause) in enumerate(zip(ids, completed.clauses)):
        content = {
            "locator": "(5.1)",
            "clause_key": clause.key,
            "source_text": clause.source_tex,
            "complete_source_sha256": completed.source_sha256,
            "proof_eligible": False,
        }
        if clause.key == "diagonal_cyclic":
            content["typed_specializations"] = typed_diagonal
        registry.add_assertion(AssertionEntry(
            assertion_id=aid,
            reference_id=ref_id,
            kind=AssertionKind.STATEMENT,
            content=content,
            origin=AssertionOrigin.SOURCE_ARCHIVE,
            component_position=i+1,
            available_after_position=None,
        ))
        records.append(MigrationRecord(
            source="phase165_r14_r22_adopted_tex",
            source_key=clause.key,
            assertion_id=aid,
            status=MigrationStatus.METADATA_ONLY,
            detail="Six-clause source completion; independent proof eligibility not granted",
        ))
    result = RegistryBridgeResult(registry, tuple(records), bridge.proof_links)
    return Toda51Integration(result, ref_id, ids,
                             len(old._references), len(old._assertions))


def audit_r22(tex_path: Path) -> dict:
    source, summary = build_phase165_r5_manifest_bridge()
    result = integrate_toda51_into_existing_reference(
        source, Path(tex_path).read_text(encoding="utf-8"),
    )
    registered = tuple(result.bridge.registry.assertion(aid)
                       for aid in result.component_ids)
    return {
        "phase": "165 R14-R22",
        "source_locator": "(5.1)",
        "existing_reference_id_reused": result.reference_id,
        "new_references": len(result.bridge.registry._references)-result.original_reference_count,
        "new_source_only_components": len(registered),
        "phase163_original_source_assertions": summary.source_assertion_count,
        "source_assertion_total": sum(
            a.origin is AssertionOrigin.SOURCE_ARCHIVE
            for a in result.bridge.registry._assertions.values()),
        "component_keys": [a.content["clause_key"] for a in registered],
        "typed_diagonal_instances": len(registered[3].content["typed_specializations"]),
        "new_proof_links": len(result.bridge.proof_links)-len(source.proof_links),
        "new_proof_eligible": 0,
        "pi32_proved": False,
        "status": "SAME_REFERENCE_SIX_CLAUSES_INTEGRATED_SOURCE_ONLY",
        "full_pytest_run": False,
    }

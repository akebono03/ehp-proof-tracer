"""Phase 165 R7: one-pass cross-index of all archived sources and proof assets.

This is an evidence-preserving inventory, NOT semantic or citation certification.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from phase163_r4_registry_bridge import RegistryBridgeResult, build_registry_bridge
from phase165_r5_manifest_bridge import DEFAULT_MANIFEST, build_phase165_r5_manifest_bridge
from phase165_r6_binding_candidates import inventory_typed_source_bindings
from unified_statement_registry import AssertionOrigin


@dataclass(frozen=True)
class BulkIntegrationResult:
    bridge: RegistryBridgeResult
    source_count: int
    candidate_pairs: tuple[tuple[str, str], ...]
    ambiguous_ids: tuple[str, ...]
    unmatched_ids: tuple[str, ...]
    repository_roots: tuple[str, ...]
    repository_root_conclusion_types: tuple[str, ...]
    verified_source_ids: tuple[str, ...] = ()
    eligible_source_ids: tuple[str, ...] = ()
    rule_expansion_provider_connected: bool = False


def build_bulk_integration(
    manifest_path: Path = DEFAULT_MANIFEST,
    *,
    proof_repository=None,
    base_bridge: RegistryBridgeResult | None = None,
) -> BulkIntegrationResult:
    """Scan all sources, typed metadata and optional repository proof roots once.

    Repository ProofSteps are internal evidence, not literature citations.
    A source-text locator match is never taken as typed mathematical equality.
    No source becomes eligible without independent review and availability.
    """
    if proof_repository is not None and base_bridge is not None:
        raise ValueError("pass either proof_repository or base_bridge, not both")
    if base_bridge is None:
        base_bridge = build_registry_bridge(proof_repository=proof_repository)
    bridge, summary = build_phase165_r5_manifest_bridge(
        manifest_path, base_bridge=base_bridge,
    )
    inventory = inventory_typed_source_bindings(bridge)
    roots = []
    types = []
    for link in bridge.proof_links:
        assertion = bridge.registry.assertion(link.assertion_id)
        if assertion.origin is not AssertionOrigin.PROOF_INTERNAL:
            raise ValueError("repository ProofStep incorrectly classified as literature")
        if link.step is None or link.step.conclusion != assertion.content:
            raise ValueError("repository ProofStep identity/conclusion mismatch")
        roots.append(link.assertion_id)
        types.append(type(link.step.conclusion).__qualname__)
    if len(set(roots)) != len(roots):
        raise ValueError("duplicate proof root")
    assert summary.newly_eligible_count == 0
    return BulkIntegrationResult(
        bridge=bridge,
        source_count=summary.source_assertion_count,
        candidate_pairs=tuple(
            (x.source_assertion_id, x.typed_assertion_id)
            for x in inventory.candidates
        ),
        ambiguous_ids=inventory.ambiguous_source_ids,
        unmatched_ids=inventory.unmatched_source_ids,
        repository_roots=tuple(roots),
        repository_root_conclusion_types=tuple(types),
    )

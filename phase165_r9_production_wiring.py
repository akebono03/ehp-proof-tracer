"""Production discovery: include adopted Toda TeX as reference source only."""
from __future__ import annotations

from dataclasses import dataclass

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r4_production_connection import discover_production_registry
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r8_rule_provider import (
    RuleCatalogReport,
    build_production_rule_provider,
)


@dataclass(frozen=True)
class ProductionGoalInputs:
    bridge: RegistryBridgeResult
    expansion_provider: object
    rule_report: RuleCatalogReport
    verified_assertion_ids: tuple[str, ...]


def discover_goal_search_inputs(*, proof_repository=None) -> ProductionGoalInputs:
    """Build all registered source records; grant no untyped ProofStep permission."""
    discovery = discover_production_registry(proof_repository=proof_repository)
    bridge, _summary = build_phase165_r5_manifest_bridge(base_bridge=discovery.bridge)
    provider, report = build_production_rule_provider()
    return ProductionGoalInputs(
        bridge=bridge,
        expansion_provider=provider,
        rule_report=report,
        verified_assertion_ids=(),
    )

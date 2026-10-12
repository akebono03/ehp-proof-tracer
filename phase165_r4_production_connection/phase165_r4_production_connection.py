"""Phase 165 R4: production registry discovery without fabricated verification.

The archive and ordinary proof repository are not verified fixed premises.
This adapter deliberately has no Phase 162 or per-group replay imports.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from phase163_r4_registry_bridge import RegistryBridgeResult, build_registry_bridge
from phase165_r3_recursive_search import GoalExpansion, RegisteredGoalUnresolved, reconstruct_registered_goal
from unified_statement_registry import AssertionOrigin


@dataclass(frozen=True)
class ProductionDiscovery:
    bridge: RegistryBridgeResult
    fixed_assertion_count: int
    internal_assertion_count: int
    archive_assertion_count: int
    proof_link_count: int
    ordered_fixed_count: int
    verified_fixed_ids: tuple[str, ...]


def discover_production_registry(*, proof_repository=None) -> ProductionDiscovery:
    """Read live production records; do not infer review approval from registration."""
    bridge = build_registry_bridge(proof_repository=proof_repository)
    assertions = tuple(bridge.registry._assertions.values())
    fixed = tuple(a for a in assertions if a.origin is AssertionOrigin.FIXED_STATEMENT)
    internal = tuple(a for a in assertions if a.origin is AssertionOrigin.PROOF_INTERNAL)
    archive = tuple(a for a in assertions if a.origin is AssertionOrigin.SOURCE_ARCHIVE)
    ordered = tuple(
        a for a in fixed
        if a.available_after_position is not None
        and bridge.registry.reference(a.reference_id).publication_position is not None
    )
    return ProductionDiscovery(
        bridge=bridge,
        fixed_assertion_count=len(fixed),
        internal_assertion_count=len(internal),
        archive_assertion_count=len(archive),
        proof_link_count=len(bridge.proof_links),
        ordered_fixed_count=len(ordered),
        verified_fixed_ids=(),
    )


def execute_production_goal(
    goal: object,
    citing_assertion_id: str,
    expansion_provider: Callable[[object], tuple[GoalExpansion, ...]],
    *,
    discovery: ProductionDiscovery,
    verified_assertion_ids: tuple[str, ...] = (),
):
    """Run R3 only with explicit review evidence, never automatic allowlisting."""
    if not isinstance(discovery, ProductionDiscovery):
        raise TypeError("discovery must be ProductionDiscovery")
    if not isinstance(verified_assertion_ids, tuple):
        raise TypeError("verified_assertion_ids must be a tuple")
    if not set(verified_assertion_ids).issubset(
        set(a.assertion_id for a in discovery.bridge.registry._assertions.values())
    ):
        raise ValueError("reviewed assertion missing from registry")
    return reconstruct_registered_goal(
        goal, discovery.bridge, citing_assertion_id, expansion_provider,
        verified_assertion_ids=verified_assertion_ids,
    )


def describe_production_blockers(discovery: ProductionDiscovery) -> tuple[str, ...]:
    """Expose actual missing safeguards rather than claiming a working solver."""
    blockers = []
    if discovery.ordered_fixed_count == 0:
        blockers.append("NO_ORDERED_FIXED_ASSERTIONS_IN_CURRENT_BRIDGE")
    if not discovery.verified_fixed_ids:
        blockers.append("NO_INDEPENDENTLY_VERIFIED_ASSERTION_IDS")
    if discovery.proof_link_count == 0:
        blockers.append("NO_LINKED_PROOF_STEPS")
    blockers.append("NO_GLOBAL_RULE_EXPANSION_PROVIDER_CONNECTED")
    return tuple(blockers)

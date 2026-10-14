"""R52-R18: optional proof-use order layered over already screened references.

This never promotes a denied source: it only removes links from an R16-screened
bridge.  A same-reference prerequisite is an explicit, reviewed proof policy,
not a claim about the order in which the reference is printed.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase163_r4_registry_bridge import RegistryBridgeResult


@dataclass(frozen=True)
class ProofUseOrder:
    """Statement IDs of permissible premises for one proof target.

    `same_reference_prerequisites` must be explicitly reviewed; the printed
    component_position is *not* interpreted as logical dependency order.
    """
    target_assertion_id: str
    same_reference_prerequisites: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.target_assertion_id, str) or not self.target_assertion_id:
            raise ValueError("target_assertion_id is required")
        if not isinstance(self.same_reference_prerequisites, tuple):
            raise TypeError("same_reference_prerequisites must be a tuple")
        if any(not isinstance(item, str) or not item for item in self.same_reference_prerequisites):
            raise ValueError("invalid prerequisite ID")
        if len(set(self.same_reference_prerequisites)) != len(self.same_reference_prerequisites):
            raise ValueError("duplicate prerequisite IDs")
        if self.target_assertion_id in self.same_reference_prerequisites:
            raise ValueError("self citation cannot be a prerequisite")


def restrict_by_proof_use_order(
    bridge: RegistryBridgeResult,
    *,
    goal: object,
    policy: ProofUseOrder,
) -> RegistryBridgeResult:
    """Restrict an already R16-screened context by reference/proof-use order.

    Cross-reference citations need both publication positions. Unknown order
    fails closed within this explicitly opted-in policy. Internal components
    of the same reference require an explicit per-goal prerequisite allowance.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if not isinstance(policy, ProofUseOrder):
        raise TypeError("policy must be ProofUseOrder")
    registry = bridge.registry
    target = registry.assertion(policy.target_assertion_id)
    destination = registry.reference(target.reference_id)
    for identifier in policy.same_reference_prerequisites:
        premise = registry.assertion(identifier)
        if premise.reference_id != target.reference_id:
            raise ValueError("same-reference prerequisite belongs to another reference")
    allowed = []
    for link in bridge.proof_links:
        cited = registry.assertion(link.assertion_id)
        if type(cited.content) is type(goal) and cited.content == goal:
            continue
        if cited.assertion_id == target.assertion_id:
            continue
        if cited.reference_id == target.reference_id:
            if cited.assertion_id in policy.same_reference_prerequisites:
                allowed.append(link)
            continue
        source = registry.reference(cited.reference_id)
        if (source.source_id and destination.source_id
                and source.source_id == destination.source_id
                and source.publication_position is not None
                and destination.publication_position is not None
                and source.publication_position < destination.publication_position):
            allowed.append(link)
    return RegistryBridgeResult(registry, bridge.records, tuple(allowed))

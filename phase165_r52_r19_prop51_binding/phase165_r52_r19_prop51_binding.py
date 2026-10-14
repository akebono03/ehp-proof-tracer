"""R52-R19: declarative proof-use prerequisites from existing typed components.

This module neither certifies citations nor creates ProofSteps.  The explicit
relations below describe proof-use order, not printed component order.
"""
from __future__ import annotations

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_r18_proof_order import ProofUseOrder


PROOF_PREREQUISITE_COMPONENTS = {
    ("Proposition 5.1", "pi3_2_group_relation"): ("eta2_hopf_relation",),
}


def resolve_registered_proof_use_order(
    bridge: RegistryBridgeResult, goal: object,
) -> ProofUseOrder | None:
    """Return a reviewed policy only for an exact, uniquely matched goal.

    The bridge must contain separately registered typed assertions with
    scope identifying their component keys.  Missing or ambiguous metadata
    grants no same-reference permissions.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    registry = bridge.registry
    matches = tuple(
        entry for entry in registry._assertions.values()
        if type(entry.content) is type(goal) and entry.content == goal
        and registry.reference(entry.reference_id).locator == "Proposition 5.1"
        and _component_key(entry) == "pi3_2_group_relation"
    )
    if not matches:
        return None
    if len(matches) != 1:
        raise ValueError("ambiguous registered proof target")
    target = matches[0]
    locator = registry.reference(target.reference_id).locator
    key = _component_key(target)
    needed = PROOF_PREREQUISITE_COMPONENTS.get((locator, key), ())
    prerequisites = []
    for component in needed:
        candidates = tuple(
            entry for entry in registry.assertions_for(target.reference_id)
            if _component_key(entry) == component
        )
        if len(candidates) != 1:
            raise ValueError("missing or ambiguous registered prerequisite: " + component)
        prerequisites.append(candidates[0].assertion_id)
    return ProofUseOrder(target.assertion_id, tuple(prerequisites))


def _component_key(entry: object) -> str | None:
    """Read component identity from established fixed-statement boundaries."""
    content = getattr(entry, "content", None)
    direct = getattr(content, "component_key", None)
    if isinstance(direct, str):
        return direct
    identifier = getattr(entry, "assertion_id", "")
    for (_, component), _prerequisites in PROOF_PREREQUISITE_COMPONENTS.items():
        if identifier.endswith(":" + component):
            return component
        for child in _prerequisites:
            if identifier.endswith(":" + child):
                return child
    return None

"""Safely expose components of independently cited GIVEN composite assertions.

This bridge does not convert legacy inferred propositions into source facts.
Existing Registry / proof links are left unmodified.
"""
from __future__ import annotations

from dataclasses import replace

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_typed_component_lookup import index_typed_components
from proof import ProofRule, ProofStep
from unified_statement_registry import AssertionOrigin, ProofStepLink, UnifiedStatementRegistry


def expand_cited_given_components(bridge: RegistryBridgeResult) -> RegistryBridgeResult:
    """Add individually searchable source claims with the same citation as the parent.

    Only an exact parent FIXED_STATEMENT -> GIVEN link authorizes a component.
    An inferred parent, missing link, duplicated link or mismatched proof is
    rejected for promotion. The original compound assertion remains available.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    registry = UnifiedStatementRegistry()
    for reference in bridge.registry._references.values():
        registry.add_reference(reference)
    for assertion in bridge.registry._assertions.values():
        registry.add_assertion(assertion)
    links = list(bridge.proof_links)
    for component in index_typed_components(bridge.registry):
        if component.component_name == "__self__":
            continue
        parent = bridge.registry.assertion(component.assertion_id)
        if parent.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        parents = tuple(link for link in bridge.proof_links if link.assertion_id == parent.assertion_id)
        if len(parents) != 1:
            continue
        parent_step = parents[0].step
        if (not isinstance(parent_step, ProofStep)
                or parent_step.rule is not ProofRule.GIVEN
                or parent_step.conclusion != parent.content
                or parent_step.premises):
            continue
        child_id = parent.assertion_id + ":component:" + component.component_name
        if child_id in registry._assertions:
            raise ValueError("component assertion ID already registered")
        registry.add_assertion(replace(
            parent, assertion_id=child_id, content=component.content,
            component_position=None,
            dependencies=(parent.assertion_id,),
        ))
        links.append(ProofStepLink(
            assertion_id=child_id,
            step=replace(parent_step, conclusion=component.content),
        ))
    return RegistryBridgeResult(registry, bridge.records, tuple(links))

"""Restore Proposition 5.1 boundaries while registering checked typed literature.

The Proposition 5.8 pi_7^3 component is adopted only after checking its
printed source and the structural generator. No proof is imported.
"""
from __future__ import annotations

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase163_r4_r11_literature_registration import register_prop56_literature_statements
from phase163_r4_r12_literature_registration import register_prop51_prop53_literature_statements
from phase165_r6_explicit_literature_inputs import prop51_prop53_inputs, prop56_inputs
from phase170_r3_r6_prop58_source import register_source_checked_prop58_pi73
from phase170_r3_r9_toda712_cited_rewrite.source712 import register_cited_toda712_generator_equality
from unified_statement_registry import UnifiedStatementRegistry


def connect_explicit_literature_components(base: RegistryBridgeResult) -> RegistryBridgeResult:
    """Register checked literature while preserving existing Proposition 5.1."""
    if not isinstance(base, RegistryBridgeResult):
        raise TypeError("base must be RegistryBridgeResult")
    first = register_prop51_prop53_literature_statements(base, prop51_prop53_inputs())
    second = register_prop56_literature_statements(first.snapshot, prop56_inputs())
    registered = register_cited_toda712_generator_equality(
        register_source_checked_prop58_pi73(second.snapshot)
    )
    if registered.proof_links != base.proof_links:
        raise ValueError("literature registration unexpectedly changed proof links")

    original = {
        assertion.assertion_id: assertion
        for assertion in base.registry._assertions.values()
        if assertion.assertion_id.startswith("boundary:Proposition 5.1:")
    }
    original_records = {
        record.assertion_id: record
        for record in base.records
        if record.assertion_id in original
    }
    registry = UnifiedStatementRegistry()
    for reference in registered.registry._references.values():
        registry.add_reference(reference)
    for assertion in registered.registry._assertions.values():
        registry.add_assertion(original.get(assertion.assertion_id, assertion))
    records = tuple(
        original_records.get(record.assertion_id, record)
        for record in registered.records
    )
    result = RegistryBridgeResult(registry, records, base.proof_links)
    for assertion_id, assertion in original.items():
        if result.registry.assertion(assertion_id) != assertion:
            raise ValueError("existing Proposition 5.1 assertion changed")
    return result

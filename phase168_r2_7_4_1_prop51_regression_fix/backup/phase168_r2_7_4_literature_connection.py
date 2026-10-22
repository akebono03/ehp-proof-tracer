"""Connect already explicit typed Toda 5.3/5.6 data to the production bridge.

No proof ancestry is imported. Registered conclusions are not proof steps.
"""
from __future__ import annotations

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase163_r4_r11_literature_registration import register_prop56_literature_statements
from phase163_r4_r12_literature_registration import register_prop51_prop53_literature_statements
from phase165_r6_explicit_literature_inputs import prop51_prop53_inputs, prop56_inputs


def connect_explicit_literature_components(base: RegistryBridgeResult) -> RegistryBridgeResult:
    """Register fixed mathematical statements, preserving all original proof links."""
    if not isinstance(base, RegistryBridgeResult):
        raise TypeError("base must be RegistryBridgeResult")
    first = register_prop51_prop53_literature_statements(base, prop51_prop53_inputs())
    second = register_prop56_literature_statements(first.snapshot, prop56_inputs())
    result = second.snapshot
    if result.proof_links != base.proof_links:
        raise ValueError("literature registration unexpectedly changed proof links")
    return result

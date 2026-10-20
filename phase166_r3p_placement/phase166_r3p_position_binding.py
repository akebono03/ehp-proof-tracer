"""Phase 166 R3-P: place two already-registered facts in proof-use order."""
from dataclasses import replace

from phase163_r4_registry_bridge import RegistryBridgeResult
from unified_statement_registry import UnifiedStatementRegistry

SUSPENSION_REF = "shared:1:adopted:ref:3"
ETA_REF = "shared:7:adopted:reference:toda5:eta_family_definition"
ETA_ASSERTION = "shared:7:adopted:assertion:toda5:eta_family_definition"
PROP51_REF = "shared:2:adopted:toda:adopted:prop5.1:finite_dimensional"
PROP51_POSITION_MAP = {
    "eta2_hopf_relation": 100,
    "pi3_2_group_relation": 200,
    "delta_iota5_relation": 400,
    "pi4_3": 500,
    "higher_eta_group_relation": 600,
}


def place_r3p_reference_positions(bridge: RegistryBridgeResult) -> RegistryBridgeResult:
    """Place foundation after (5.1) and eta notation inside Proposition 5.1.

    Only reference positions and canonical assertion positions change. Existing
    IDs, mathematical statements, source records, and proof links are retained.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    for ref_id, expected in ((SUSPENSION_REF, "Foundational: suspension identity"),
                             (ETA_REF, "Chapter V, i)"),
                             (PROP51_REF, "Proposition 5.1")):
        ref = bridge.registry.reference(ref_id)
        if expected not in ref.locator:
            raise ValueError(f"unexpected R3-P source: {ref_id}")
    if bridge.registry.reference(PROP51_REF).publication_position != 7800:
        raise ValueError("Proposition 5.1 must already be at publication_position=7800")
    reference_updates = {SUSPENSION_REF: 7701, ETA_REF: 7800}
    assertion_updates = {ETA_ASSERTION: 300}
    for key, position in PROP51_POSITION_MAP.items():
        assertion_id = "shared:2:toda:adopted:prop5.1:" + key
        assertion = bridge.registry.assertion(assertion_id)
        prior = 100 if key == "eta2_hopf_relation" else (
            200 if key == "pi3_2_group_relation" else (
                300 if key == "delta_iota5_relation" else (
                    400 if key == "pi4_3" else 500)))
        if assertion.component_position not in (prior, position):
            raise ValueError(f"unexpected existing component position: {assertion_id}")
        assertion_updates[assertion_id] = position
    eta = bridge.registry.assertion(ETA_ASSERTION)
    if eta.reference_id != ETA_REF or eta.component_position not in (None, 300):
        raise ValueError("eta-family statement identity or order changed")
    result = UnifiedStatementRegistry()
    for reference in bridge.registry._references.values():
        position = reference_updates.get(reference.reference_id)
        result.add_reference(replace(reference, publication_position=position) if position is not None else reference)
    for assertion in bridge.registry._assertions.values():
        position = assertion_updates.get(assertion.assertion_id)
        result.add_assertion(replace(assertion, component_position=position) if position is not None else assertion)
    return RegistryBridgeResult(result, bridge.records, bridge.proof_links)

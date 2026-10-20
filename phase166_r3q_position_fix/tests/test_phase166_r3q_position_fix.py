"""R3-Q: canonical and split-component publication positions."""
from dataclasses import replace

import pytest

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3p_position_binding import PROP51_POSITION_MAP, place_r3p_reference_positions
from phase163_r4_registry_bridge import RegistryBridgeResult
from unified_statement_registry import UnifiedStatementRegistry


def test_split_components_match_canonical_positions():
    bridge = build_shared_typed_bridge()
    parent = "shared:2:toda:adopted:prop5.1:finite_dimensional"
    assert bridge.registry.assertion(parent).component_position is None
    for key, position in PROP51_POSITION_MAP.items():
        if key == "pi4_3":
            continue
        canonical = bridge.registry.assertion("shared:2:toda:adopted:prop5.1:" + key)
        child = bridge.registry.assertion(parent + ":component:" + key)
        assert child.component_position == canonical.component_position == position
        assert child.content == canonical.content


def test_pi32_can_cite_earlier_hopf_component_but_not_later_delta():
    bridge = build_shared_typed_bridge()
    parent = "shared:2:toda:adopted:prop5.1:finite_dimensional"
    target = "shared:2:toda:adopted:prop5.1:pi3_2_group_relation"
    assert precedes_citing_assertion(bridge, parent + ":component:eta2_hopf_relation", target)
    assert not precedes_citing_assertion(bridge, parent + ":component:delta_iota5_relation", target)


def test_position_binding_is_idempotent():
    bridge = build_shared_typed_bridge()
    again = place_r3p_reference_positions(bridge)
    assert again.registry._assertions == bridge.registry._assertions
    assert again.proof_links == bridge.proof_links


def test_conflicting_child_content_is_rejected():
    bridge = build_shared_typed_bridge()
    child_id = "shared:2:toda:adopted:prop5.1:finite_dimensional:component:eta2_hopf_relation"
    reg = UnifiedStatementRegistry()
    for ref in bridge.registry._references.values():
        reg.add_reference(ref)
    for assertion in bridge.registry._assertions.values():
        reg.add_assertion(replace(assertion, content="incorrect") if assertion.assertion_id == child_id else assertion)
    invalid = RegistryBridgeResult(reg, bridge.records, bridge.proof_links)
    with pytest.raises(ValueError, match="component does not match"):
        place_r3p_reference_positions(invalid)

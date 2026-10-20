from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3p_position_binding import (
    ETA_ASSERTION, ETA_REF, PROP51_REF, SUSPENSION_REF,
)


def test_r3p_order_placement_and_source_identity():
    bridge = build_shared_typed_bridge()
    assert bridge.registry.reference(SUSPENSION_REF).publication_position == 7701
    assert bridge.registry.reference(ETA_REF).publication_position == 7800
    assert bridge.registry.reference(PROP51_REF).publication_position == 7800
    expected = {
        "eta2_hopf_relation": 100,
        "pi3_2_group_relation": 200,
        "delta_iota5_relation": 400,
        "pi4_3": 500,
        "higher_eta_group_relation": 600,
    }
    for key, position in expected.items():
        assertion = bridge.registry.assertion("shared:2:toda:adopted:prop5.1:" + key)
        assert assertion.component_position == position
        assert assertion.reference_id == PROP51_REF
    eta = bridge.registry.assertion(ETA_ASSERTION)
    assert eta.component_position == 300
    assert eta.reference_id == ETA_REF
    assert "Toda_05_2.tex" in bridge.registry.reference(ETA_REF).source_id


def test_r3p_order_comparison():
    bridge = build_shared_typed_bridge()
    pi32 = "shared:2:toda:adopted:prop5.1:pi3_2_group_relation"
    delta = "shared:2:toda:adopted:prop5.1:delta_iota5_relation"
    higher = "shared:2:toda:adopted:prop5.1:higher_eta_group_relation"
    assert precedes_citing_assertion(bridge, pi32, ETA_ASSERTION)
    assert precedes_citing_assertion(bridge, ETA_ASSERTION, delta)
    assert precedes_citing_assertion(bridge, ETA_ASSERTION, higher)
    assert not precedes_citing_assertion(bridge, higher, ETA_ASSERTION)


def test_r3p_foundation_is_before_prop51():
    bridge = build_shared_typed_bridge()
    foundation = "shared:1:adopted:assertion:3"
    pi32 = "shared:2:toda:adopted:prop5.1:pi3_2_group_relation"
    assert precedes_citing_assertion(bridge, foundation, pi32)

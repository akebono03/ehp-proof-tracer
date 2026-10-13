from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r14_r12_registry_obligations import bind_delta_zero_obligations, audit_r12
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap, TodaSuspensionIsomorphismStatement


def test_two_distinct_necessary_subgoals():
    bridge, _ = build_phase165_r5_manifest_bridge()
    items = bind_delta_zero_obligations(bridge)
    assert len(items) == 2
    assert items[0].label == "E_pi11_pi22_isomorphism"
    assert items[1].label == "Delta_E_exactness"


def test_iso_requires_derived_evidence_not_false_literature_fact():
    bridge, _ = build_phase165_r5_manifest_bridge()
    e = bind_delta_zero_obligations(bridge)[0]
    assert e.goal == TodaSuspensionIsomorphismStatement(
        TodaSuspensionMap(TodaPrimaryGroup(1, 1), TodaPrimaryGroup(2, 2)))
    assert e.source_assertion_ids == ()
    assert "DERIVED_GOAL" in e.origin


def test_exactness_archive_is_not_certified():
    bridge, _ = build_phase165_r5_manifest_bridge()
    e = bind_delta_zero_obligations(bridge)[1]
    assert e.source_locator == "Proposition 4.2"
    assert e.status == "NOT_PROOF_ELIGIBLE"
    assert all(identifier.startswith("phase163:archive:") for identifier in e.source_assertion_ids)


def test_registry_is_unchanged():
    bridge, _ = build_phase165_r5_manifest_bridge()
    before = (len(bridge.registry._references), len(bridge.registry._assertions), len(bridge.proof_links))
    bind_delta_zero_obligations(bridge)
    assert before == (len(bridge.registry._references), len(bridge.registry._assertions), len(bridge.proof_links))


def test_no_proof_step_or_false_completion():
    report = audit_r12()
    assert report["registered_proof_eligible"] == 0
    assert report["toda_proof_steps_created"] == 0
    assert report["pi32_proved"] is False

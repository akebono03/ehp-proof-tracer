"""R12-R8 focused provenance and type audit tests."""
from dataclasses import replace

from phase165_r12_r8_typed_source_connection import collect_permitted_typed_source_anchors
from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
from phase165_r52_r12_component_bridge import expand_cited_given_components
from phase165_r12_r7_proof_order_guard import restrict_registered_ordered_claims
from phase165_prop51_claim_order import pi4_3_goal
from proof import ProofRule, ProofStep


def _screened():
    bridge = expand_cited_given_components(build_adopted_prop51_reference())
    # R7 normally operates on prefixed IDs from build_shared_typed_bridge.
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    return restrict_registered_ordered_claims(
        build_shared_typed_bridge(sources=(build_adopted_prop51_reference(),)),
        pi4_3_goal(),
    )


def test_r8_permitted_sources_do_not_include_root_or_future():
    anchors = collect_permitted_typed_source_anchors(_screened())
    ids = tuple(a.assertion_id for a in anchors)
    assert not any("higher_eta_group_relation" in identifier for identifier in ids)
    assert not any("pi4_3_group_relation" in identifier for identifier in ids)
    assert not any(identifier.endswith(":finite_dimensional") for identifier in ids)
    assert all(anchor.step.rule is ProofRule.GIVEN for anchor in anchors)


def test_r8_permitted_prior_source_claims_are_traced():
    anchors = collect_permitted_typed_source_anchors(_screened())
    identifiers = tuple(a.assertion_id for a in anchors)
    assert any("eta2_hopf_relation" in name for name in identifiers)
    assert any("pi3_2_group_relation" in name for name in identifiers)
    assert any("delta_iota5_relation" in name for name in identifiers)


def test_r8_inferred_fact_cannot_become_source_anchor():
    bridge = _screened()
    replaced = replace(bridge, proof_links=tuple(
        replace(link, step=ProofStep(link.step.conclusion, (), ProofRule.INFERENCE))
        for link in bridge.proof_links
    ))
    assert collect_permitted_typed_source_anchors(replaced) == ()


def test_r8_duplicate_source_id_fails_closed():
    bridge = _screened()
    with_duplicate = replace(bridge, proof_links=bridge.proof_links + bridge.proof_links[:1])
    import pytest
    with pytest.raises(ValueError, match="duplicate typed proof witness"):
        collect_permitted_typed_source_anchors(with_duplicate)

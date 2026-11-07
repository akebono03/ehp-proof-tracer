"""Focused public proof-frontier integration: no completion claim."""
from __future__ import annotations

from phase174_r3_r7_r15_chain_frontier_audit.audit import inspect_live_chain


def test_canonical_chain_has_only_independent_candidate_obligations() -> None:
    live = inspect_live_chain()
    assert live["public_source_n6_inference_ancestry_checked"] is True
    assert live["canonical_family_identity_exact"] is True
    assert live["prior_result_is_candidate_not_verified_proof"] is True
    assert live["new_verified_proof_steps"] == 0
    assert live["new_group_given"] == 0
    assert live["completion_claimed"] is False
    assert live["production_files_changed"] is False
    assert live["public_provider_changed"] is False
    isolated = live["isolated_existing_general_candidates"]
    assert isolated == {
        "cyclic_generator_to_zero_image": 1,
        "composite_zero_to_generator_zero": 1,
        "rebracket_composite_image": 1,
        "decompose_composite_image": 1,
    }
    for key in (
        "source_n6_annihilator", "suspension_image_zero", "generator_image_zero",
        "generator_image_left_composite", "generator_image_right_composite",
        "final_pi12_7_zero",
    ):
        assert key not in live["direct_given_intermediate_names"]
    frontiers = live["public_goal_frontiers"]
    source = frontiers["source_n6_annihilator"]
    assert any(item["rule"] == source["named_rule"] for item in source["proposals"])
    assert "stage" in frontiers["suspension_image_zero"]
    assert "stage" in frontiers["generator_image_zero"]

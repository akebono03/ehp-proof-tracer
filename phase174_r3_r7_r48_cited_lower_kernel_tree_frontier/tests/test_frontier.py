"""R48 requires genuine canonical R35 kernel proof with two cited prior leaves."""
from __future__ import annotations

from phase174_r3_r7_r48_cited_lower_kernel_tree_frontier.audit import (
    inspect_integrated_lower_kernel_frontier,
)


def test_canonical_kernel_proof_is_inferred_from_three_cited_parents() -> None:
    report = inspect_integrated_lower_kernel_frontier()
    assert report["canonical_status"] == "partial"
    assert report["canonical_lower_kernel_inference_count"] == 1
    assert report["canonical_lower_kernel_three_premises_cited"] is True
    assert report["canonical_lower_kernel_domain_inferred"] is True
    assert len(report["canonical_lower_kernel_prior_reference_ids"]) == 2
    assert report["kernel_was_not_adopted_as_given"] is True


def test_zero_image_and_hopf_inference_survive_the_kernel_connection() -> None:
    report = inspect_integrated_lower_kernel_frontier()
    assert report["canonical_zero_image_inference_count"] == 1
    assert report["canonical_hopf_injectivity_inference_count"] == 1
    assert report["canonical_hopf_has_toda59_and_prop42_ancestors"] is True
    assert report["canonical_lower_image_kernel_inference_count"] == 1
    assert report["canonical_lower_image_kernel_has_prop42_ancestor"] is True
    assert report["canonical_verified_steps"] > 14


def test_prop27_frontier_is_left_unresolved_without_false_completion() -> None:
    report = inspect_integrated_lower_kernel_frontier()
    assert report["canonical_visited_prop27_frontier"] is True
    assert report["canonical_open_goal_types"].get("Prop27TypedHopfDeltaStatement", 0) >= 1
    assert report["root_complete"] is False
    assert report["wrong_pi10_5_group_zero_proved"] is False
    assert report["new_givens"] == 0
    assert report["new_mathematical_rules"] == 0
    assert report["production_files_changed"] == 0
    assert report["web_http_checked"] is False
    assert report["full_pytest"] is False

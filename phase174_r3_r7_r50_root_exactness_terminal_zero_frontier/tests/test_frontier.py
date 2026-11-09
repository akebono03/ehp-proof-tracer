"""R50 requires a real certified group-zero root, not just a candidate."""
from __future__ import annotations

from phase174_r3_r7_r50_root_exactness_terminal_zero_frontier.audit import (
    inspect_integrated_root_frontier,
)


def test_both_root_exactness_windows_are_cited_inferences() -> None:
    report = inspect_integrated_root_frontier()
    assert report["canonical_root_delta_e_exactness_inference_count"] == 1
    assert report["canonical_root_e_h_exactness_inference_count"] == 1
    assert report["canonical_root_exactness_has_prop42_ancestors"] is True
    assert report["source_first_general_prop42_given"] == 1


def test_terminal_zero_is_inferred_from_general_toda51() -> None:
    report = inspect_integrated_root_frontier()
    assert report["canonical_terminal_group_coordinates"] == [12, 13]
    assert report["canonical_terminal_zero_inference_count"] == 1
    assert report["canonical_terminal_zero_has_toda51_ancestor"] is True
    assert report["canonical_toda51_general_source_reference_id"]


def test_final_group_zero_root_has_four_inferred_parents_and_all_citations() -> None:
    report = inspect_integrated_root_frontier()
    assert report["canonical_status"] == "complete"
    assert report["canonical_root_inference_count"] == 1
    assert report["canonical_root_four_independent_inference_parents"] is True
    assert report["canonical_root_has_all_six_cited_facts"] is True
    assert report["canonical_root_verified_complete"] is True
    assert report["root_complete"] is True
    assert report["canonical_upper_delta_surjectivity_inference_count"] == 1
    assert report["canonical_prop27_cited_three_level_ancestry"] is True
    assert report["canonical_lower_kernel_three_premises_cited"] is True


def test_root_zero_inference_does_not_bypass_references_or_claim_web() -> None:
    report = inspect_integrated_root_frontier()
    assert report["new_givens"] == 0
    assert report["new_mathematical_rules"] == 0
    assert report["production_files_changed"] == 0
    assert report["wrong_pi10_5_group_zero_proved"] is False
    assert report["isolated_proof_steps_injected"] is False
    assert report["web_http_checked"] is False
    assert report["full_pytest"] is False

"""Proposition 2.7 joins the real R48 search through R37 upper Delta."""
from __future__ import annotations

from phase174_r3_r7_r49_prop27_upper_delta_tree_frontier.audit import (
    inspect_integrated_prop27_frontier,
)


def test_typed_prop27_has_genuine_cited_three_level_proof() -> None:
    report = inspect_integrated_prop27_frontier()
    assert report["source_first_toda59_given"] == 1
    assert report["source_first_general_prop42_given"] == 1
    assert report["canonical_prop27_typed_inference_count"] == 1
    assert report["canonical_prop27_general_inference_count"] == 1
    assert report["canonical_prop27_cited_three_level_ancestry"] is True
    assert report["canonical_prop27_source_reference_id"]
    assert report["canonical_visited_prop27_frontier"] is True


def test_upper_delta_has_four_independent_inferred_parents() -> None:
    report = inspect_integrated_prop27_frontier()
    assert report["canonical_status"] == "partial"
    assert report["canonical_upper_delta_surjectivity_inference_count"] == 1
    assert report["canonical_upper_delta_four_independent_inference_parents"] is True
    assert report["canonical_visited_root_exactness_frontier"] is True
    assert report["canonical_lower_kernel_inference_count"] == 1
    assert report["canonical_lower_kernel_three_premises_cited"] is True
    assert report["canonical_hopf_injectivity_inference_count"] == 1


def test_bounded_r49_never_claims_final_zero_group_or_fabricated_source() -> None:
    report = inspect_integrated_prop27_frontier()
    assert report["root_complete"] is False
    assert report["new_givens"] == 0
    assert report["new_mathematical_rules"] == 0
    assert report["production_files_changed"] == 0
    assert report["isolated_proof_steps_injected"] is False
    assert report["wrong_pi10_5_group_zero_proved"] is False
    assert report["web_http_checked"] is False
    assert report["full_pytest"] is False

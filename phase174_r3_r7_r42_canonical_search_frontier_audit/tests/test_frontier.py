"""Real scoped canonical-search results, with both missing public bridges explicit."""
from __future__ import annotations

from phase174_r3_r7_r42_canonical_search_frontier_audit.audit import inspect_search_frontier
from phase174_r3_r7_r42_canonical_search_frontier_audit.source_guard import verify_checkout


def test_r42_source_guard_accepts_only_reviewed_r41_handoff():
    state = verify_checkout()
    assert state["source_guard"] == "PASS"
    assert state["reviewed_merge_paths"] == 16
    assert state["production_files_changed"] == 0


def test_public_zero_image_candidate_exists_but_upper_delta_wiring_is_absent():
    result = inspect_search_frontier()
    assert result["screened_toda59_sources"] == 1
    assert result["public_root_ehp_candidates"] == 1
    assert result["public_zero_image_r41_candidates"] == 1
    assert result["isolated_upper_delta_r37_candidates"] == 1
    assert result["public_upper_delta_r37_candidates"] == 0


def test_real_canonical_scoped_search_fails_closed_without_forged_proof():
    result = inspect_search_frontier()
    assert result["adopted_db_prior_verified_for_group_root"] is True
    assert result["direct_zero_image_goal_admits_db_prior"] is False
    assert result["canonical_root_scoped_search_status"] == "search_failed"
    assert result["canonical_root_scoped_verified_steps"] == 0
    assert result["canonical_root_scoped_open_upper_delta"] is True
    assert result["canonical_zero_image_scoped_status"] == "search_failed"
    assert result["scoped_probe_not_full_web_search"] is True
    assert result["new_given_statements"] == 0
    assert result["root_complete"] is False

"""Verify actual public R5/R37 options and bounded canonical-search scope."""
from __future__ import annotations

from phase174_r3_r7_r43_public_ehp_map_property_wiring.audit import (
    inspect_public_ehp_frontier,
)


def test_public_r5_and_r37_conditional_candidates_are_present():
    observed = inspect_public_ehp_frontier()
    assert observed["screened_toda59_source_leaves"] == 1
    assert observed["public_ehp_root_candidates"] == 1
    assert observed["public_upper_delta_r37_candidates"] == 1
    assert observed["public_hopf_injectivity_r5_candidates"] == 1
    assert observed["public_adopted_db_zero_image_r41_candidates"] == 1
    assert observed["r37_independent_subgoals"] == 4
    assert observed["r5_independent_subgoals"] == 2


def test_scoped_search_admits_authentic_db_under_group_root_only():
    observed = inspect_public_ehp_frontier()
    assert observed["root_scoped_db_prior_admitted_by_actual_search"] is True
    assert observed["direct_zero_image_scope_db_prior_admitted"] is False
    assert observed["scoped_canonical_verified_db_prior_steps"] == 1
    assert observed["scoped_canonical_generator_zero_open"] is True
    assert observed["scoped_canonical_search_status"] == "partial"


def test_no_public_root_proof_or_fabricated_source_is_claimed():
    observed = inspect_public_ehp_frontier()
    assert observed["new_given_statements"] == 0
    assert observed["new_mathematical_rules"] == 0
    assert observed["r40_isolated_result_not_promoted_to_public_proof"] is True
    assert observed["upper_delta_surjectivity_verified"] is False
    assert observed["root_complete"] is False
    assert observed["web_http_checked"] is False
    assert observed["full_pytest"] is False

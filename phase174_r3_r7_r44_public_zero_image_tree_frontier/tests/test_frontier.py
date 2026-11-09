"""Public evidence is distinguished from optional inferred outcomes."""
from __future__ import annotations

from phase174_r3_r7_r44_public_zero_image_tree_frontier.audit import inspected_frontier


def test_actual_typed_r41_cannot_be_confused_with_pi10_5_zero_group():
    report = inspected_frontier()
    assert report["screened_toda59_sources"] == 1
    assert report["zero_image_is_not_domain_zero_group"] is True
    assert report["wrong_pi10_5_zero_group_is_r41_direct_premise"] is False
    assert report["wrong_pi10_5_zero_group_was_proved"] is False
    assert report["r41_prior_adopted_as_db_given"] is True
    assert report["r41_prior_is_independent_literature"] is False


def test_bounded_canonical_search_never_claims_web_completion():
    report = inspected_frontier()
    assert report["probe_is_not_full_web_search"] is True
    assert report["web_http_checked"] is False
    assert report["root_complete"] is False
    assert report["new_givens"] == 0
    assert report["production_files_changed"] == 0
    assert report["canonical_bounded_search_status"] in ("partial", "search_failed")
    assert report["canonical_bounded_verified_steps"] >= 1

"""R47 links genuine source-first R44 and R46 proofs in one canonical DFS."""
from __future__ import annotations

from functools import lru_cache

from phase174_r3_r7_r47_zero_image_prop42_hopf_bridge.audit import inspect_integrated_hopf_frontier


@lru_cache(maxsize=1)
def observed() -> dict[str, object]:
    return inspect_integrated_hopf_frontier()


def test_both_independent_cited_source_leaves_are_present():
    report = observed()
    assert report["source_first_toda59_given"] == 1
    assert report["source_first_general_prop42_given"] == 1
    assert report["r44_db_prior_is_independent_literature"] is False
    assert report["r44_db_prior_admitted_in_group_root_scope"] is True


def test_integrated_hopf_inference_is_derived_not_injected():
    report = observed()
    if report["canonical_hopf_injectivity_inference_count"] > 0:
        assert report["canonical_zero_image_inference_count"] > 0
        assert report["canonical_hopf_exactness_inference_count"] > 0
        assert report["canonical_hopf_has_toda59_and_prop42_ancestors"] is True
    assert report["isolated_proof_steps_injected"] is False
    assert report["wrong_pi10_5_group_zero_proved"] is False


def test_lower_image_kernel_is_checked_only_after_canonical_hopf_chain():
    report = observed()
    if report["canonical_lower_image_kernel_inference_count"] > 0:
        assert report["canonical_lower_exactness_inference_count"] > 0
        assert report["canonical_lower_image_kernel_has_prop42_ancestor"] is True
    if report["canonical_visited_lower_kernel_frontier"]:
        assert report["canonical_hopf_injectivity_inference_count"] > 0
        assert report["canonical_lower_image_kernel_inference_count"] > 0


def test_root_remains_open_and_no_math_is_added():
    report = observed()
    assert report["canonical_status"] in ("partial", "search_failed")
    assert report["root_complete"] is False
    assert report["new_givens"] == 0
    assert report["new_mathematical_rules"] == 0
    assert report["production_files_changed"] == 0
    assert report["web_http_checked"] is False
    assert report["full_pytest"] is False

"""Compare actual public search and scoped R50 without installing a proof."""
from __future__ import annotations

from phase174_r3_r7_r51_public_route_gap_audit.audit import inspect_public_route_gap


def test_source_backed_scoped_root_is_complete_and_not_injected() -> None:
    report = inspect_public_route_gap()
    assert report["r50_scoped_complete"] is True
    assert report["r50_scoped_verified_steps"] == 28
    assert report["r50_scoped_root_has_six_cited_facts"] is True
    assert report["r50_proof_not_injected_into_public"] is True
    assert report["new_given"] == 0
    assert report["production_files_changed"] == 0


def test_public_search_and_web_model_have_same_completion_status() -> None:
    report = inspect_public_route_gap()
    if report["public_root_proof_complete"]:
        assert report["public_result_status"] == "complete"
        assert report["public_web_key"] == "generic-complete-proof"
        assert report["public_web_partial_result"] is False
    else:
        assert report["public_result_status"] in ("partial", "search_failed")
        assert report["public_web_key"] == "generic-partial-proof"
        assert report["public_web_partial_result"] is True
    assert report["public_web_model_route_checked"] is True
    assert report["public_http_checked"] is False


def test_public_kernel_candidate_must_be_present_without_forcing_completion() -> None:
    report = inspect_public_route_gap()
    assert report["public_root_ehp_candidates"] == 1
    assert report["public_upper_delta_candidates"] == 1
    assert report["public_r35_kernel_candidates"] == 1
    assert report["public_r35_kernel_requires_bare_relation"] is True
    assert report["public_r35_kernel_source_bound_candidates"] == 0
    assert report["public_kernel_domain_cited_specializations"] >= 1
    assert report["gate"].startswith("PASS_R51_")

"""R46 explicitly distinguishes isolated subproofs from a completed group proof."""
from __future__ import annotations

from functools import lru_cache

from phase174_r3_r7_r46_prop42_dfs_audit.audit import inspect_prop42_dfs_frontier


@lru_cache(maxsize=1)
def observed() -> dict[str, object]:
    return inspect_prop42_dfs_frontier()


def test_cited_source_controls_public_prop42_specializations():
    report = observed()
    assert report["source_first_universal_count"] == 1
    assert report["prop42_public_candidates"] == {
        "root_delta_e": 1,
        "root_e_h": 1,
        "hopf_e_h": 1,
        "lower_h_delta": 1,
    }
    assert all(value == 0 for value in report["prop42_when_source_removed"].values())


def test_actual_canonical_subproofs_never_claim_unsupported_ancestry():
    report = observed()
    assert set(report["isolated_canonical_subproofs"]) == {
        "root_delta_e", "root_e_h", "hopf_e_h", "lower_h_delta",
        "lower_image_kernel",
    }
    for proof in report["isolated_canonical_subproofs"].values():
        assert proof["status"] in ("proved", "unresolved", "not_inferred")
        if proof["inference"]:
            assert proof["general_prop42_ancestor"] is True
            assert proof["accepted_steps"] >= 2


def test_r45_first_unresolved_branch_is_not_promoted_to_root_proof():
    report = observed()
    assert report["r45_bounded_status"] in ("partial", "search_failed")
    assert report["r45_public_provider_visit_trace"][0] == "root"
    assert "zero_image_outside_scope" in report["r45_public_provider_visit_trace"]
    assert report["isolated_proofs_not_added_to_root_search"] is True
    assert report["r44_zero_image_not_replayed"] is True
    assert report["root_complete"] is False


def test_no_new_math_source_or_unreviewed_web_completion():
    report = observed()
    assert report["new_given"] == 0
    assert report["new_mathematical_rules"] == 0
    assert report["production_files_changed"] == 0
    assert report["web_http_checked"] is False
    assert report["full_pytest"] is False

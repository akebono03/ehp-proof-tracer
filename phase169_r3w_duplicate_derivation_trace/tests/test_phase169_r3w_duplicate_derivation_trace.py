"""Read-only verification of actual proof ambiguity candidates."""
from __future__ import annotations

import pytest

from phase169_r3w_duplicate_derivation_trace.audit import examine


@pytest.fixture(scope="module")
def report():
    return examine()


def test_pi53_baseline_preserved(report):
    assert report["pi53_status"] == "complete"
    assert not report["production_modified"]
    assert not report["existing_tests_modified"]
    assert not report["full_pytest_run"]


def test_all_accepted_candidates_are_real_verified_steps(report):
    assert report["provider_proposal_count"] >= 1
    assert report["verified_candidate_count"] >= report["verified_candidate_kept_count"]
    assert all(item["rule"] == "inference" for item in report["verified_candidate_attempts"])
    assert all(item["given_leaves"] for item in report["verified_candidate_attempts"])


def test_ambiguity_is_recorded_without_selecting_a_proof(report):
    if "found 2" in report["pi65_proof_status"]:
        assert report["verified_candidate_kept_count"] <= 2
        assert report["verified_candidate_kept_count"] + len(report["screened_direct_pi65_given_assertions"]) >= 2
    assert report["mode"] == "AUDIT_ONLY"

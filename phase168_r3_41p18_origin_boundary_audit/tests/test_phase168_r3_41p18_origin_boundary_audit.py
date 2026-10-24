"""Read-only regression assertions on a freshly executed R3-41P18 audit."""
from __future__ import annotations

import json

import pytest

from phase168_r3_41p18_origin_boundary_audit.audit import CASES, OUTPUT


@pytest.fixture(scope="module")
def report():
    path = OUTPUT / "audit.json"
    if not path.is_file():
        pytest.fail("Run `python -m phase168_r3_41p18_origin_boundary_audit.audit` first")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["phase"] == "168 R3-41P18"
    assert data["status"] == "ORIGIN_BOUNDARY_GAPS_CONFIRMED"
    return data


@pytest.mark.parametrize("name,n,k,inference,given", CASES)
def test_canonical_groups_remain_identical(report, name, n, k, inference, given):
    row = report["cases"][name]
    assert row["expected_counts"] == [inference, given]
    assert row["inference_count"] == inference
    assert row["given_count"] == given
    assert row["same_step_objects"]
    assert row["fulltext_equal"]
    assert row["web_fulltext_equal"]
    assert row["citations_equal"]
    assert row["web_citations_equal"]
    assert not row["web_partial"]
    assert row["all_invariants_pass"]


def test_historical_observation_is_closed(report):
    assert all(row["closed_observation_rejected"] for row in report["cases"].values())


def test_self_attestation_is_not_a_trustworthy_certificate(report):
    limits = report["limits"]
    assert limits["forged_step_unseen_before_notes"]
    assert limits["forged_step_rejected_before_notes"]
    assert limits["self_attested_forged_inference_accepted"]


def test_result_target_and_bridge_identity_are_not_bound(report):
    limits = report["limits"]
    assert limits["inconsistent_result_target_accepted"]
    assert limits["replacement_bridge_wrapper_accepted"]
    assert limits["cross_search_bridge_rejected"]


def test_origin_scope_is_not_one_search_invocation(report):
    limits = report["limits"]
    assert limits["observation_aggregates_multiple_searches"]
    assert limits["nested_cannot_reuse_outer_observation"]
    assert limits["nested_does_not_inherit_outer_steps"]
    assert limits["outer_observation_restored"]
    assert limits["manual_observation_rejected"]


def test_no_application_files_or_baselines_modified(report):
    assert report["source_sha256_before"] == report["source_sha256_after"]

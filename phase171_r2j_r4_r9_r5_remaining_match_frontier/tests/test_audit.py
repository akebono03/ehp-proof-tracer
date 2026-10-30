"""Focused diagnostic classifications and genuine R9-R4 replay."""
from __future__ import annotations

import pytest

from phase171_r2j_r4_r9_r5_remaining_match_frontier.audit import (
    _classify_match_attempt,
    _git,
    _proof_event,
    inspect_remaining_match_frontier,
)
from proof import ProofRule, ProofStep


def _record(matches=0, expected=None, actual=None, expected_conclusions=None,
            actual_conclusions=None):
    return {
        "matches": matches,
        "expected_proof_rules": ["inference"] if expected is None else expected,
        "actual_proof_rules": ["given"] if actual is None else actual,
        "expected_conclusions": ["same"] if expected_conclusions is None else expected_conclusions,
        "actual_conclusions": ["same"] if actual_conclusions is None else actual_conclusions,
    }


def test_reports_proof_rule_mismatch_when_conclusions_are_equal():
    assert _classify_match_attempt(_record()) == "PREMISE_PROOF_RULE_MISMATCH"


def test_reports_distinct_conclusions_before_any_proof_status_diagnosis():
    assert _classify_match_attempt(_record(
        expected_conclusions=["x"], actual_conclusions=["y"],
    )) == "PREMISE_CONCLUSION_MISMATCH"


def test_same_premise_types_and_results_mean_guard_or_pattern_rejection():
    assert _classify_match_attempt(_record(
        expected=["inference"], actual=["inference"],
    )) == "MATCHER_PATTERN_OR_GUARD_REJECTION"


def test_accepted_match_is_never_classified_as_failure():
    assert _classify_match_attempt(_record(matches=1)) == "MATCH_ACCEPTED"


def test_search_events_reject_fabricated_proved_event():
    with pytest.raises(TypeError):
        _proof_event("proved", "goal", None)
    with pytest.raises(ValueError):
        _proof_event("invalid", "goal", None)


def test_search_event_records_real_inference_not_new_given():
    step = ProofStep("group", (), ProofRule.INFERENCE)
    actual = _proof_event("proved", "group", step)
    assert actual["proof_rule"] == "inference"
    assert actual["kind"] == "proved"
    unresolved = _proof_event("unresolved", "missing", None)
    assert unresolved["proof_rule"] is None


def test_read_only_git_allowlist_rejects_mutation():
    with pytest.raises(ValueError):
        _git("reset", "--hard")


def test_live_scoped_replay_preserves_hopf_repair_and_source_boundary():
    report = inspect_remaining_match_frontier()
    assert report["hopf_surjectivity_rebuilt"] is True
    assert report["inferred_rule_catalog"] >= 3
    assert report["new_given_added"] == 0
    assert report["public_provider_modified"] is False
    assert report["public_web_verified"] is False
    assert report["canonical_search_status"] in ("complete", "partial")
    if report["trust_boundary_accepted"]:
        assert report["canonical_search_status"] == "complete"

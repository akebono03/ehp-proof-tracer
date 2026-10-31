"""R15 tests: audit-log interpretation is non-mutating and fail-closed."""
from __future__ import annotations

from copy import deepcopy

import pytest

from phase171_r2j_r4_r9_r15_branch_blocker_audit.audit import (
    analyze_r14,
    blob_sha,
    candidate_observation,
    checked_r14_report,
    git_read,
    matches_goal,
    normalize,
    route_signature,
)


def fixture_r14():
    root = {"role": "root", "goal": "root", "count": 2, "proposals": [
        {"rule": "root-a", "subgoals": ["A"]},
        {"rule": "root-b", "subgoals": ["B"]},
    ]}
    return {
        "phase": "171-R2J-R4-R9-R14",
        "mode": "READ_ONLY_CANONICAL_BRANCH_EXCEPTION_TRACE",
        "tracked_status_unchanged": True,
        "source_changes": 0,
        "new_given": 0,
        "completed_proof_imported": False,
        "git_head": "f" * 40,
        "provider_events": [root, {"role": "other", "goal": "A", "count": 0, "rules": []}],
        "exception_events": [
            {"origin": True, "kind": "no_derivation", "target_role": "other",
             "target": "A", "active_roles": ["root", "other"],
             "active_last": ["root", "A"], "candidate_rule": "",
             "accepted_options_so_far": 0},
            {"origin": False, "kind": "no_derivation", "target_role": "root",
             "target": "root", "candidate_rule": "root-a",
             "candidate_subgoals": ["A"]},
            {"origin": True, "kind": "no_derivation", "target_role": "other",
             "target": "A", "active_roles": ["root", "other"],
             "active_last": ["root", "A"], "candidate_rule": "",
             "accepted_options_so_far": 0},
            {"origin": False, "kind": "no_derivation", "target_role": "root",
             "target": "root", "candidate_rule": "root-b",
             "candidate_subgoals": ["B"]},
        ],
        "provider_events_dropped": 0,
        "exception_events_dropped": 0,
        "origin_counts": {"no_derivation": 2},
        "root_route_count": 2,
        "public_status": "partial",
        "first_open_is_reverse": True,
    }


def test_valid_r14_contract_and_deduplication():
    raw = fixture_r14()
    before = deepcopy(raw)
    report = analyze_r14(raw)
    assert raw == before
    assert report["r14_root_routes"] == 2
    assert report["unique_no_derivation_goal_count"] == 1
    assert report["no_derivation_event_count"] == 2
    assert report["blocker_classes"] == {"NO_EXPANSION": 1}
    assert report["classification"] == "UNIQUE_GOALS_WITH_ZERO_PROVIDER_EXPANSIONS"
    assert report["ranked_no_derivation_goals"][0]["count"] == 2


def test_root_branches_preserve_order_and_propagation_counts():
    report = analyze_r14(fixture_r14())
    assert [route["rule"] for route in report["root_branches"]] == ["root-a", "root-b"]
    assert [route["propagated_failures"] for route in report["root_branches"]] == [
        {"no_derivation": 1}, {"no_derivation": 1},
    ]


def test_candidate_with_proposals_is_not_labeled_missing():
    provider = [{"goal": "Relation(xxxxxxxxx)", "count": 1, "rules": ["rule-a"]}]
    result = candidate_observation({"target": "Relation(xxxxxxxxx) and tail"}, provider)
    assert result["observation"] == "PROPOSALS_UNPROVED"
    assert result["rule_names"] == ["rule-a"]
    assert matches_goal("Relation(xxxxxxxxx)", "Relation(xxxxxxxxx) and tail")
    assert not matches_goal("", "anything")
    assert route_signature("r", ["x"]) != route_signature("r", ["y"])


def test_incomplete_or_modified_r14_trace_fails_closed():
    raw = fixture_r14()
    raw["exception_events_dropped"] = 1
    with pytest.raises(ValueError, match="truncated"):
        checked_r14_report(raw)
    raw = fixture_r14()
    raw["source_changes"] = 1
    with pytest.raises(ValueError, match="source_changes"):
        checked_r14_report(raw)
    raw = fixture_r14()
    raw["origin_counts"]["no_derivation"] = 3
    with pytest.raises(ValueError, match="origin count"):
        analyze_r14(raw)


def test_no_new_derivation_is_inferred_from_missing_provider_trace():
    raw = fixture_r14()
    raw["provider_events"] = raw["provider_events"][:1]
    report = analyze_r14(raw)
    assert report["blocker_classes"] == {"NOT_OBSERVED": 1}
    assert "None:" in report["causal_claim"]


def test_read_only_git_guard_and_normalization():
    with pytest.raises(ValueError, match="read-only"):
        git_read("reset", "--hard")
    assert normalize(b"\xef\xbb\xbfabc\r\n") == "abc\n"
    assert blob_sha(b"test\n") == "9daeafb9864cf43055ae93beb0afd6c7d144bfa4"

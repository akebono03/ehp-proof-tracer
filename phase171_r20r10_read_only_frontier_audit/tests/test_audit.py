"""Focused, self-contained tests for the R20R10 observer and source guard."""
from __future__ import annotations

import hashlib

from phase171_r20r10_read_only_frontier_audit.audit import (
    PublicTrace,
    distinct_goals,
    git_blob_sha,
    reviewed_blob_matches,
)


def test_git_blob_hash_matches_specification() -> None:
    data = b"hello\n"
    expected = hashlib.sha1(b"blob 6\0" + data).hexdigest()
    assert git_blob_sha(data) == expected
    assert reviewed_blob_matches(data, expected)


def test_newlines_tolerated_but_code_changes_rejected() -> None:
    expected = git_blob_sha(b"a\nb\n")
    assert reviewed_blob_matches(b"a\r\nb\r\n", expected)
    assert not reviewed_blob_matches(b"a\nbb\n", expected)


def test_unique_goals_use_exact_type_and_equality() -> None:
    assert distinct_goals([3, True, 3, True, "3"]) == [3, True, "3"]


def test_instrumentation_delegates_and_preserves_original_results() -> None:
    trace = PublicTrace()
    seen = []

    class Option:
        def __init__(self, rule, subgoals):
            self.rule = rule
            self.subgoals = subgoals

    class Rule:
        name = "test inference"

    def expand(goal):
        seen.append(("provider", goal))
        return (Option(Rule(), ("earlier",)),)

    def original(goal, bridge, citation, provider, **kwargs):
        options = provider(goal)
        assert len(options) == 1
        kwargs["progress_observer"]("unresolved", "earlier", None)
        kwargs["progress_observer"]("proved", goal, object())
        return "canonical-result"

    def observer(kind, goal, step):
        seen.append((kind, goal))

    returned = trace.traced_reconstruct(
        original, "goal", object(), "source-id", expand,
        progress_observer=observer, lookup_mode="typed_reference_publication",
    )
    assert returned == "canonical-result"
    assert seen == [
        ("provider", "goal"), ("unresolved", "earlier"), ("proved", "goal"),
    ]
    assert trace.has("unresolved", "earlier")
    assert trace.has("proved", "goal")
    assert len(trace.expanded) == 1
    assert trace.events[0]["kind"] == "search_root"
    assert trace.events[1]["kind"] == "expand"


def test_unresolved_classification_distinguishes_missing_and_failed_premises() -> None:
    trace = PublicTrace()
    trace.expanded.append(("no-route", ()))
    class Rule:
        name = "candidate"

    class Option:
        rule = Rule()
        subgoals = ("subgoal",)

    trace.expanded.append(("has-route", (Option(),)))
    trace.unresolved.extend(("no-route", "has-route"))
    summary = trace.unresolved_summary()
    assert [x["classification"] for x in summary] == [
        "NO_BACKWARD_PROPOSAL", "PREMISE_OR_INFERENCE_NOT_COMPLETED",
    ]

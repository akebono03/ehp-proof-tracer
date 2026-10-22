"""Focused tests for the read-only R1 audit report helpers."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit import describe, goal_report, result_report


def test_goal_report_preserves_candidate_count():
    report = goal_report(("first", "second"))
    assert report["count"] == 2
    assert report["candidates"] == ["'first'", "'second'"]


def test_result_report_does_not_invent_completion():
    class Partial:
        status = "PARTIAL"
        proven_steps = ()
        open_goals = ("unresolved",)
        diagnostics = ("not proved",)

    report = result_report(Partial())
    assert report["status"] == "PARTIAL"
    assert report["proven_count"] == 0
    assert report["open_goals"] == ["'unresolved'"]
    assert report["diagnostics"] == ["not proved"]


def test_describe_truncation_is_explicit():
    assert "TRUNCATED" in describe("x" * 100, limit=12)

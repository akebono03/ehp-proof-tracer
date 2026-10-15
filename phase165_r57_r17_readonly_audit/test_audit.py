"""Focused tests for the read-only diagnostic's pure reporting helpers."""
from __future__ import annotations

import ast
from pathlib import Path

from audit import render_report, safe_string, summarize_result


HERE = Path(__file__).resolve().parent


def test_safe_string_handles_unprintable_objects():
    class Broken:
        def __str__(self):
            raise RuntimeError("broken")
    assert "string-error" in safe_string(Broken())


def test_result_summary_for_incomplete_proof():
    class Result:
        status = "search_failed"
        conclusion = None
        proven_steps = ()
        open_goals = ("unresolved",)
        diagnostics = ("no rule",)
    result = summarize_result(Result())
    assert result["proven_step_count"] == 0
    assert result["open_goals"] == ["unresolved"]


def test_report_identifies_each_goal_and_prior_count():
    report = render_report({
        "bridge": {"assertions": 2},
        "targets": [{"group": "pi_5^4", "candidate_count": 1,
                     "result": {"status": "search_failed", "proven_step_count": 0}}],
        "search_calls": [{"n": 4, "k": 1, "prior_completed_count": 0,
                          "screened_reference_links": 4, "root_expansion_count": 0}],
    })
    assert "pi_5^4" in report
    assert "prior=0" in report
    assert "root_expansions=0" in report


def test_audit_does_not_mutate_repository_sources():
    source = (HERE / "audit.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
    assert not any(isinstance(node.func, ast.Attribute) and node.func.attr in {
        "replace_function", "write_bytes", "unlink", "rename", "replace",
    } for node in calls)
    assert "patch.object(shared, \"search_registered_partial_proof\"" in source

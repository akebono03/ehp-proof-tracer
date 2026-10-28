"""Focused offline R3-R1 tests: fail-closed provenance and honest diagnosis."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest


def load_audit():
    path = Path(__file__).resolve().parents[1] / "audit.py"
    spec = importlib.util.spec_from_file_location("phase170_r3_r1_local_audit", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_r3_target_scope_is_only_five_previous_failures():
    audit = load_audit()
    assert audit.TARGETS == ((3, 3), (4, 3), (5, 3), (4, 4), (5, 4))
    assert len(audit.ALL_CASES) == 12


def test_r3_git_added_audit_packages_only():
    audit = load_audit()
    assert audit.allowed_later_files(())
    assert audit.allowed_later_files((("A", "phase170_r2_head_sync_r1/run.ps1"),))
    assert not audit.allowed_later_files((("M", "phase170_r2_head_sync_r1/run.ps1"),))
    assert not audit.allowed_later_files((("A", "phase165_r55_nk_only_goal.py"),))
    assert not audit.allowed_later_files((("A", "phase170_r2_head_sync_r1/../other.py"),))


def test_r3_rejects_malformed_git_name_status():
    audit = load_audit()
    assert audit.parse_name_status_z(b"A\0path.txt\0") == (("A", "path.txt"),)
    with pytest.raises(ValueError, match="malformed"):
        audit.parse_name_status_z(b"A\0")


def test_r3_unpositioned_target_is_not_called_math_failure():
    audit = load_audit()
    row = audit.infer_frontier(
        {"status": "search_failed", "open_goals": [{"type": "Relation"}], "proof_step_count": 0},
        {"selected_goal_count": 1, "selector_errors": []}, None,
    )
    assert row["observed_category"] == "DERIVED_TARGET_SCREENING_AND_INFERENCE_UNRESOLVED"
    assert row["mathematical_theorem_missing_certified"] is False
    assert row["renderer_only_defect_certified"] is False


def test_r3_positioned_target_is_not_automatically_complete():
    audit = load_audit()
    row = audit.infer_frontier(
        {"status": "search_failed", "open_goals": [], "proof_step_count": 0},
        {"selected_goal_count": 1, "selector_errors": []}, "assertion-1",
    )
    assert row["observed_category"] == "POSITIONED_TARGET_INFERENCE_UNRESOLVED"
    assert row["positioned_citing_assertion"]


def test_r3_missing_and_ambiguous_goal_are_distinct():
    audit = load_audit()
    r1 = {"status": "search_failed", "open_goals": [], "proof_step_count": 0}
    assert audit.infer_frontier(r1, {"selected_goal_count": 0}, None)["observed_category"] == "GOAL_NOT_SELECTED"
    assert audit.infer_frontier(r1, {"selected_goal_count": 2}, None)["observed_category"] == "GOAL_NOT_UNIQUE"
    assert audit.infer_frontier(r1, {"selected_goal_count": 1, "selector_errors": ["x"]}, None)["observed_category"] == "GOAL_SELECTOR_EXCEPTION"


def test_r3_rejects_r1_missing_graph(tmp_path: Path):
    audit = load_audit()
    with pytest.raises(RuntimeError, match="missing"):
        audit.load_trace(tmp_path / "audit.json", 3, 3, 0)


def test_r3_r1_trace_checks_dependency_indices(tmp_path: Path):
    audit = load_audit()
    report = tmp_path / "audit.json"
    trace = tmp_path / "pi6_3_trace.json"
    content = {"step_graph": [{"index": 0, "premises": [9]}]}
    trace.write_text(json.dumps(content), encoding="utf-8")
    with pytest.raises(RuntimeError, match="invalid dependency"):
        audit.load_trace(report, 3, 3, 1)
    content["step_graph"][0]["premises"] = []
    trace.write_text(json.dumps(content), encoding="utf-8")
    result = audit.load_trace(report, 3, 3, 1)
    assert result["steps"] == content["step_graph"]


def test_r3_crosschecks_live_selector_and_recorded_citations():
    audit = load_audit()
    r1 = {"group": "pi_6^3", "n": 3, "k": 3, "status": "search_failed", "classification": "SEARCH_FAILED"}
    r2 = {"selected_goal_count": 1, "selected_goal_citations": [{"citing_assertion_id": None}],
          "blocker_classification": "SOURCE_ORDER_OR_CITATION_DIAGNOSTIC"}
    graph = {"step_count": 0}
    screen = {"typed_goal_count": 1, "citation_ids": [None], "source_screen_mode": "x"}
    out = audit.report_case(r1, r2, graph, screen)
    assert out["frontier"]["mathematical_theorem_missing_certified"] is False
    screen["citation_ids"] = ["different"]
    with pytest.raises(RuntimeError, match="citation resolution differs"):
        audit.report_case(r1, r2, graph, screen)


def test_r3_markdown_reports_uncertainty():
    audit = load_audit()
    report = {"git": {"head": "abc"}, "r1_report": "r1", "r2_report": "r2",
              "tracked_unchanged": True, "cases": []}
    text = audit.markdown(report)
    assert "不足定理" in text
    assert "全体 pytest" in text

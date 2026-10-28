"""Focused tests for R4's read-only validation helpers."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from phase169_phase_closeout_r4_safe_docs_commit.run import (
    DOC_BLOBS,
    DOC_MARKER,
    DOCS,
    R1_HEAD,
    REVIEWED_HEAD,
    locate_full_copy,
    validate_report,
)


def make_report(tmp_path: Path) -> dict:
    log_a = tmp_path / "focused.log"
    log_b = tmp_path / "active_full.log"
    log_a.write_text("67 passed in 21.86s\n", encoding="utf-8")
    log_b.write_text("3546 passed in 34.95s\n", encoding="utf-8")
    return {
        "mode": "PHASE169_END_OF_PHASE_TEST",
        "head": R1_HEAD,
        "reviewed_files": 13,
        "r6_cases": 19,
        "focused": {"command": ["python", "-B", "-m", "pytest", "-p", "no:cacheprovider", "a.py"], "exit_code": 0, "passed_count": 67, "log": str(log_a)},
        "active_full": {"command": ["python", "-B", "-m", "pytest", "-p", "no:cacheprovider", "tests"], "exit_code": 0, "passed_count": 3546, "log": str(log_b)},
        "git_index_preserved": True,
        "phase169_certified": False,
        "phase169_test_gate_pass": True,
        "decision": "TEST_GATE_PASS_PENDING_PHASE169_CLOSEOUT_DOCUMENTATION",
    }


def test_reviewed_docs_and_head_are_exact():
    assert len(DOCS) == 5
    assert set(DOCS) == set(DOC_BLOBS)
    assert len(REVIEWED_HEAD) == 40
    assert len(R1_HEAD) == 40
    assert DOC_MARKER.startswith("<!-- PHASE169")


def test_verified_report_is_accepted(tmp_path: Path):
    validate_report(make_report(tmp_path))


def test_incorrect_pass_count_is_rejected(tmp_path: Path):
    report = make_report(tmp_path)
    report["active_full"]["passed_count"] = 3545
    with pytest.raises(RuntimeError, match="active_full"):
        validate_report(report)


def test_false_test_gate_is_rejected(tmp_path: Path):
    report = make_report(tmp_path)
    report["phase169_test_gate_pass"] = False
    with pytest.raises(RuntimeError, match="phase169_test_gate_pass"):
        validate_report(report)


def test_wrong_head_is_rejected(tmp_path: Path):
    report = make_report(tmp_path)
    report["head"] = "0" * 40
    with pytest.raises(RuntimeError, match="head"):
        validate_report(report)


def test_missing_log_is_rejected(tmp_path: Path):
    report = make_report(tmp_path)
    Path(report["focused"]["log"]).unlink()
    with pytest.raises(RuntimeError, match="log"):
        validate_report(report)


def test_failing_log_is_rejected(tmp_path: Path):
    report = make_report(tmp_path)
    Path(report["focused"]["log"]).write_text("1 failed, 67 passed in 21s\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="failure"):
        validate_report(report)


def test_nonnumeric_pass_count_is_rejected(tmp_path: Path):
    report = make_report(tmp_path)
    report["focused"]["passed_count"] = True
    with pytest.raises(RuntimeError, match="focused"):
        validate_report(report)


def test_wrong_test_scope_is_rejected(tmp_path: Path):
    report = make_report(tmp_path)
    report["active_full"]["command"][-1] = "."
    with pytest.raises(RuntimeError, match="scope"):
        validate_report(report)


def test_full_copy_lookup_with_original_paths(tmp_path: Path):
    full = tmp_path / "after_full"
    nested = full / "docs" / "roadmap.md"
    nested.parent.mkdir(parents=True)
    nested.write_text("test\n", encoding="utf-8")
    assert locate_full_copy(full, "docs/roadmap.md") == nested


def test_full_copy_lookup_rejects_missing(tmp_path: Path):
    with pytest.raises(RuntimeError, match="Expected unique"):
        locate_full_copy(tmp_path, "README.md")

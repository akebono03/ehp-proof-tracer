"""R4A narrow verifier tests: no production files or historical tests changed."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from phase169_phase_closeout_r4a_committed_document_audit.run import (
    AUDIT_PACKAGE_PATHS,
    DOCUMENT_BLOBS,
    EXPECTED_COMMIT_PATHS,
    FINAL_HEAD,
    PARENT_HEAD,
    R1_DIR,
    TEST_HEAD,
    verify_commit_scope,
    verify_test_report,
)


def sample_report(recovery: Path) -> dict:
    folder = recovery / R1_DIR
    folder.mkdir(parents=True)
    focused = folder / "focused_pytest.log"
    active = folder / "active_full_pytest.log"
    focused.write_text("67 passed in 21.86s\n", encoding="utf-8")
    active.write_text("3546 passed in 34.95s\n", encoding="utf-8")
    return {
        "mode": "PHASE169_END_OF_PHASE_TEST",
        "head": TEST_HEAD,
        "reviewed_files": 13,
        "r6_cases": 19,
        "git_index_preserved": True,
        "phase169_certified": False,
        "phase169_test_gate_pass": True,
        "decision": "TEST_GATE_PASS_PENDING_PHASE169_CLOSEOUT_DOCUMENTATION",
        "focused": {
            "exit_code": 0, "passed_count": 67,
            "command": ["python", "-B", "-m", "pytest", "-p", "no:cacheprovider", "f.py"],
            "log": str(focused),
        },
        "active_full": {
            "exit_code": 0, "passed_count": 3546,
            "command": ["python", "-B", "-m", "pytest", "-p", "no:cacheprovider", "tests"],
            "log": str(active),
        },
    }


def test_fixed_committed_scope():
    assert len(FINAL_HEAD) == 40
    assert len(PARENT_HEAD) == 40
    assert len(DOCUMENT_BLOBS) == 5
    assert len(AUDIT_PACKAGE_PATHS) == 16
    assert len(EXPECTED_COMMIT_PATHS) == 21


def test_commit_scope_accepts_verified_paths():
    verify_commit_scope(set(EXPECTED_COMMIT_PATHS))


def test_commit_scope_rejects_extra_path():
    with pytest.raises(RuntimeError, match="inventory"):
        verify_commit_scope(set(EXPECTED_COMMIT_PATHS) | {"web_group_proof.py"})


def test_commit_scope_rejects_missing_document():
    with pytest.raises(RuntimeError, match="inventory"):
        verify_commit_scope(set(EXPECTED_COMMIT_PATHS) - {"README.md"})


def test_report_accepts_verified_gate(tmp_path: Path):
    report = sample_report(tmp_path)
    assert verify_test_report(report, tmp_path) == {"focused": 67, "active_full": 3546}


def test_report_rejects_failed_gate(tmp_path: Path):
    report = sample_report(tmp_path)
    report["phase169_test_gate_pass"] = False
    with pytest.raises(RuntimeError, match="phase169_test_gate_pass"):
        verify_test_report(report, tmp_path)


def test_report_rejects_mismatched_head(tmp_path: Path):
    report = sample_report(tmp_path)
    report["head"] = "0" * 40
    with pytest.raises(RuntimeError, match="head"):
        verify_test_report(report, tmp_path)


def test_report_rejects_wrong_full_count(tmp_path: Path):
    report = sample_report(tmp_path)
    report["active_full"]["passed_count"] = 3545
    with pytest.raises(RuntimeError, match="active_full"):
        verify_test_report(report, tmp_path)


def test_report_rejects_missing_log(tmp_path: Path):
    report = sample_report(tmp_path)
    Path(report["focused"]["log"]).unlink()
    with pytest.raises(RuntimeError, match="log"):
        verify_test_report(report, tmp_path)


def test_report_rejects_wrong_scope(tmp_path: Path):
    report = sample_report(tmp_path)
    report["active_full"]["command"][-1] = "."
    with pytest.raises(RuntimeError, match="scope"):
        verify_test_report(report, tmp_path)


def test_report_rejects_log_failure(tmp_path: Path):
    report = sample_report(tmp_path)
    Path(report["focused"]["log"]).write_text("1 failed, 67 passed in 20s\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="failures"):
        verify_test_report(report, tmp_path)


def test_report_rejects_boolean_exit_code(tmp_path: Path):
    report = sample_report(tmp_path)
    report["focused"]["exit_code"] = False
    with pytest.raises(RuntimeError, match="focused"):
        verify_test_report(report, tmp_path)

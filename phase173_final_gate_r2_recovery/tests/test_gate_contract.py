"""Corrective phase-end gate contracts: exact fixes, evidence and retry safety."""
from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase173_final_gate_r2_recovery import gate


def test_reviewed_replacement_hashes_match_r1_source() -> None:
    reviewed = Path(__file__).resolve().parents[1] / "reviewed_test_replacements"
    for path, digest in gate.REPAIRED_TEST_SHA256.items():
        assert gate.normalized_digest((reviewed / Path(path).name).read_bytes()) == digest


def test_line_ending_only_differences_produce_equal_hash() -> None:
    content = b"a = 1\nb = 2\n"
    windows = b"a = 1\r\nb = 2\r\n"
    assert gate.normalized_digest(content) == gate.normalized_digest(windows)


def test_actual_statement_edits_do_not_pass_digest() -> None:
    assert gate.normalized_digest(b"a = 1\n") != gate.normalized_digest(b"a = 2\n")


def test_reviewed_history_allows_only_gate_packages_and_three_fixes() -> None:
    assert gate.permitted_committed_changes([
        "tests/test_phase167_r2_range_dedup.py",
        "phase173_final_gate/run.ps1",
        "phase173_final_gate_r1_phase167_reference_contract/README.md",
        "phase173_final_gate_r2_recovery/gate.py",
    ])
    assert not gate.permitted_committed_changes([
        "phase168_r3_5_model_renderer.py",
    ])


def _prior_files(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    payload = {
        "phase": 173,
        "head": gate.REVIEWED_BASE,
        "status": "FAIL",
        "pytest_exit_code": 1,
    }
    (directory / "phase173_full_test_report.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )
    output = "\n".join(
        "FAILED " + name.replace("/", "\\")
        for name in gate.EXPECTED_PREVIOUS_FAILURES
    ) + "\n5 failed, 3541 passed in 34.43s\n"
    (directory / "active_suite_stdout.txt").write_text(output, encoding="utf-8")
    (directory / "active_suite_stderr.txt").write_text("", encoding="utf-8")
    (directory / "phase173_full_test_attempt.json").write_text(
        '{"status":"STARTED"}', encoding="utf-8"
    )


def test_prior_failure_evidence_is_read_only_and_complete(tmp_path: Path) -> None:
    _prior_files(tmp_path)
    before = (tmp_path / "phase173_full_test_report.json").read_bytes()
    hashes = gate.verify_prior_failure(tmp_path)
    assert len(hashes) == 4
    assert hashes["phase173_full_test_report.json"] == gate.sha256_file(
        tmp_path / "phase173_full_test_report.json"
    )
    assert (tmp_path / "phase173_full_test_report.json").read_bytes() == before


def test_prior_failure_rejects_missing_expected_case(tmp_path: Path) -> None:
    _prior_files(tmp_path)
    file = tmp_path / "active_suite_stdout.txt"
    file.write_text("5 failed, 3541 passed in 34.43s\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Missing reviewed failure"):
        gate.verify_prior_failure(tmp_path)


def test_prior_failure_rejects_wrong_result_status(tmp_path: Path) -> None:
    _prior_files(tmp_path)
    file = tmp_path / "phase173_full_test_report.json"
    report = json.loads(file.read_text(encoding="utf-8"))
    report["status"] = "PASS"
    file.write_text(json.dumps(report), encoding="utf-8")
    with pytest.raises(RuntimeError, match="does not match"):
        gate.verify_prior_failure(tmp_path)


def test_summary_requires_exact_active_count() -> None:
    count, summary = gate.parse_success_summary(
        "..... [100%]\n3546 passed in 51.20s\n", 0
    )
    assert count == gate.EXPECTED_ACTIVE_PASSED
    assert summary == "3546 passed in 51.20s"
    with pytest.raises(ValueError, match="count changed"):
        gate.parse_success_summary("3545 passed in 51.20s\n", 0)


def test_summary_rejects_nonzero_exit_and_bad_counts() -> None:
    with pytest.raises(ValueError, match="code zero"):
        gate.parse_success_summary("5 failed, 3541 passed in 34.43s", 1)
    with pytest.raises(ValueError, match="not found"):
        gate.parse_success_summary("no completed test summary", 0)


def _snapshot() -> dict[str, object]:
    return {
        "head": gate.REVIEWED_BASE,
        "git_index_tree": "reviewed-git-index-tree",
        "reviewed_blob_count": 15,
        "repaired_test_count": 3,
    }


def test_exclusive_attempt_refuses_duplicate(tmp_path: Path) -> None:
    attempt = tmp_path / "attempt.json"
    gate.start_attempt(attempt, _snapshot(), {"old": "sha256"})
    assert json.loads(attempt.read_text(encoding="utf-8"))["status"] == "STARTED"
    with pytest.raises(FileExistsError):
        gate.start_attempt(attempt, _snapshot(), {"old": "sha256"})


def test_success_report_is_recorded_once_and_matched(tmp_path: Path) -> None:
    snapshot = _snapshot()
    prior = {"old": "sha256"}
    attempt = tmp_path / "attempt.json"
    report_file = tmp_path / "report.json"
    stdout = tmp_path / "stdout.txt"
    stderr = tmp_path / "stderr.txt"
    gate.start_attempt(attempt, snapshot, prior)
    stdout.write_text("3546 passed in 36.00s\n", encoding="utf-8")
    stderr.write_text("", encoding="utf-8")
    report = gate.finalize(snapshot, prior, attempt, report_file, stdout, stderr, 0)
    assert report["status"] == "PASS"
    assert report["phase_formally_closed"] is False
    assert gate.validate_recorded_success(report_file, snapshot, prior) is True
    with pytest.raises(RuntimeError, match="refusing to replace"):
        gate.finalize(snapshot, prior, attempt, report_file, stdout, stderr, 0)


def test_failed_corrective_run_still_saves_distinct_report(tmp_path: Path) -> None:
    snapshot = _snapshot()
    attempt = tmp_path / "attempt.json"
    report_file = tmp_path / "report.json"
    stdout = tmp_path / "stdout.txt"
    stderr = tmp_path / "stderr.txt"
    prior = {"old": "sha256"}
    gate.start_attempt(attempt, snapshot, prior)
    stdout.write_text("1 failed, 3545 passed in 36.00s", encoding="utf-8")
    stderr.write_text("", encoding="utf-8")
    recorded = gate.finalize(snapshot, prior, attempt, report_file, stdout, stderr, 1)
    assert recorded["status"] == "FAIL"
    with pytest.raises(RuntimeError, match="not a matching success"):
        gate.validate_recorded_success(report_file, snapshot, prior)


def test_stale_prior_evidence_cannot_be_reused(tmp_path: Path) -> None:
    snapshot = _snapshot()
    attempt = tmp_path / "attempt.json"
    report_file = tmp_path / "report.json"
    stdout = tmp_path / "stdout.txt"
    stderr = tmp_path / "stderr.txt"
    gate.start_attempt(attempt, snapshot, {"old": "sha256"})
    stdout.write_text("3546 passed in 36.00s", encoding="utf-8")
    stderr.write_text("", encoding="utf-8")
    with pytest.raises(RuntimeError, match="does not match"):
        gate.finalize(snapshot, {"old": "different"}, attempt,
                      report_file, stdout, stderr, 0)
    assert not report_file.exists()


def test_snapshot_checks_guarded_changes_with_mock_git(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    original = dict(gate.REPAIRED_TEST_SHA256)
    try:
        for path in original:
            location = tmp_path / path
            location.parent.mkdir(parents=True, exist_ok=True)
            location.write_bytes(b"reviewed = True\r\n")
        monkeypatch.setattr(
            gate, "REPAIRED_TEST_SHA256",
            {key: gate.normalized_digest(b"reviewed = True\n") for key in original},
        )
        def mocked_git(repo: Path, *args: str, allow_nonzero: bool = False):
            if args == ("rev-parse", "--show-toplevel"):
                value = str(repo)
            elif args == ("branch", "--show-current"):
                value = "develop"
            elif args == ("rev-parse", "HEAD"):
                value = gate.REVIEWED_BASE
            elif args == ("rev-parse", "origin/develop"):
                value = gate.REVIEWED_BASE
            elif args[0] == "rev-parse" and args[1].startswith("HEAD:"):
                value = gate.REVIEWED_BLOBS[args[1][5:]]
            elif args[:2] == ("diff", "--name-only"):
                value = "\n".join(original.keys())
            elif args == ("write-tree",):
                value = "mock-index-tree"
            else:
                value = ""
            return SimpleNamespace(stdout=value, returncode=0, stderr="")
        monkeypatch.setattr(gate, "git", mocked_git)
        snapshot = gate.validate_snapshot(tmp_path)
        assert snapshot["repaired_test_count"] == 3
        assert snapshot["reviewed_blob_count"] == 15
    finally:
        gate.REPAIRED_TEST_SHA256.clear()
        gate.REPAIRED_TEST_SHA256.update(original)

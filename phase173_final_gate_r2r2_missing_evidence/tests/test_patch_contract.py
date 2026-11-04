"""Focused tests for the opt-in missing-historical-evidence R2R2 patch."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil

import pytest

from phase173_final_gate_r2r2_missing_evidence import patch


PACKAGE = Path(__file__).resolve().parents[1]
REPLACEMENT_GATE = PACKAGE / "replacement" / "gate.py"
REPLACEMENT_RUNNER = PACKAGE / "replacement" / "run.ps1"
ORIGINAL_BACKUP = PACKAGE / "tests" / "fixtures"


def _gate():
    spec = importlib.util.spec_from_file_location("r2r2_reviewed_gate", REPLACEMENT_GATE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _valid_prior(gate, directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "phase173_full_test_report.json").write_text(
        json.dumps({"phase": 173, "head": gate.REVIEWED_BASE,
                    "status": "FAIL", "pytest_exit_code": 1}), encoding="utf-8"
    )
    output = "\n".join("FAILED " + name.replace("/", "\\")
                       for name in gate.EXPECTED_PREVIOUS_FAILURES)
    (directory / "active_suite_stdout.txt").write_text(
        output + "\n5 failed, 3541 passed in 34.43s\n", encoding="utf-8"
    )
    (directory / "active_suite_stderr.txt").write_text("", encoding="utf-8")
    (directory / "phase173_full_test_attempt.json").write_text(
        json.dumps({"status": "STARTED"}), encoding="utf-8"
    )


def test_reviewed_sources_have_pinned_hashes_and_valid_python() -> None:
    import ast
    ast.parse(REPLACEMENT_GATE.read_text(encoding="utf-8"))
    assert set(patch.ORIGINAL_SHA256) == {"gate.py", "run.ps1"}
    for name in patch.ORIGINAL_SHA256:
        assert patch.digest(REPLACEMENT_GATE.read_bytes() if name == "gate.py"
                            else REPLACEMENT_RUNNER.read_bytes()) == patch.REPLACEMENT_SHA256[name]
        assert len(patch.ORIGINAL_SHA256[name]) == 64


def test_default_mode_still_rejects_absent_evidence(tmp_path: Path) -> None:
    gate = _gate()
    with pytest.raises(RuntimeError, match="evidence is incomplete"):
        gate.verify_prior_failure(tmp_path)


def test_explicit_missing_mode_returns_no_hashes_without_writes(tmp_path: Path) -> None:
    gate = _gate()
    prior = tmp_path / "other_profile"
    assert gate.verify_prior_failure(prior, allow_missing=True) == {}
    assert not prior.exists()
    assert gate.prior_evidence_status({}) == "UNAVAILABLE_ORIGINAL_FILES"


def test_partial_originals_never_accepted_even_with_opt_in(tmp_path: Path) -> None:
    gate = _gate()
    (tmp_path / "active_suite_stdout.txt").write_text("", encoding="utf-8")
    with pytest.raises(RuntimeError, match="evidence is incomplete"):
        gate.verify_prior_failure(tmp_path, allow_missing=True)


def test_verified_four_file_evidence_remains_verified(tmp_path: Path) -> None:
    gate = _gate()
    _valid_prior(gate, tmp_path)
    found = gate.verify_prior_failure(tmp_path, allow_missing=True)
    assert len(found) == 4
    assert all(len(x) == 64 for x in found.values())
    assert gate.prior_evidence_status(found) == "VERIFIED_FOUR_FILES"


def test_invalid_complete_baseline_is_not_accepted(tmp_path: Path) -> None:
    gate = _gate()
    _valid_prior(gate, tmp_path)
    (tmp_path / "active_suite_stdout.txt").write_text("5 failed, 3541 passed\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Missing reviewed failure"):
        gate.verify_prior_failure(tmp_path, allow_missing=True)


def test_run_requires_explicit_missing_evidence_switch() -> None:
    script = REPLACEMENT_RUNNER.read_text(encoding="utf-8")
    assert "[switch]$AllowMissingPriorEvidence" in script
    assert "if ($AllowMissingPriorEvidence)" in script
    assert "--allow-missing-prior-evidence" in script
    assert "@PriorArguments --attempt" in script
    assert "Partial previous evidence" in script
    assert script.count("@PriorArguments --attempt") == 3


def test_missing_evidence_is_not_claimed_as_verified_in_public_gate() -> None:
    source = REPLACEMENT_GATE.read_text(encoding="utf-8")
    assert '("PASS" if prior_hashes else "NOT_VERIFIABLE")' in source
    assert '"NOT_VERIFIABLE"' in source
    assert '"prior_failure_evidence_status": prior_evidence_status(prior_hashes)' in source
    assert "return {}" in source


def test_gate_preserves_full_suite_size_and_reviewed_source_checks() -> None:
    gate = _gate()
    assert gate.EXPECTED_ACTIVE_PASSED == 3546
    assert len(gate.REVIEWED_BLOBS) == 15
    assert len(gate.REPAIRED_TEST_SHA256) == 3
    assert gate.parse_success_summary("3546 passed in 47.03s", 0)[0] == 3546
    with pytest.raises(ValueError):
        gate.parse_success_summary("3541 passed in 47.03s", 0)


def test_reviewed_two_file_patcher_is_idempotent_and_restores_backup(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    target = repo / patch.TARGET_DIR
    target.mkdir(parents=True)
    pack = tmp_path / "package"
    (pack / "replacement").mkdir(parents=True)
    for name in patch.ORIGINAL_SHA256:
        original = ORIGINAL_BACKUP / name
        assert patch.digest(original.read_bytes()) == patch.ORIGINAL_SHA256[name]
        shutil.copyfile(original, target / name)
        shutil.copyfile(PACKAGE / "replacement" / name, pack / "replacement" / name)
    result = patch.apply_reviewed_patch(repo, pack)
    assert len(result) == 2
    assert patch.apply_reviewed_patch(repo, pack) == ()
    assert len(patch.rollback_reviewed_patch(repo, pack)) == 2
    for name in patch.ORIGINAL_SHA256:
        assert patch.digest((target / name).read_bytes()) == patch.ORIGINAL_SHA256[name]


def test_patcher_refuses_unknown_changes(tmp_path: Path) -> None:
    target = tmp_path / patch.TARGET_DIR
    target.mkdir()
    (target / "gate.py").write_text("tampered", encoding="utf-8")
    (target / "run.ps1").write_bytes(REPLACEMENT_RUNNER.read_bytes())
    with pytest.raises(RuntimeError, match="unreviewed"):
        patch.reviewed_files(tmp_path, PACKAGE)


def test_unavailable_prior_still_writes_honest_new_report(tmp_path: Path) -> None:
    gate = _gate()
    snapshot = {"head": gate.REVIEWED_BASE, "remote_head": gate.REVIEWED_BASE,
                "git_index_tree": "tree123", "reviewed_blob_count": 15,
                "repaired_test_count": 3}
    attempt = tmp_path / "attempt.json"
    report = tmp_path / "report.json"
    stdout = tmp_path / "stdout.txt"
    stderr = tmp_path / "stderr.txt"
    gate.start_attempt(attempt, snapshot, {})
    stdout.write_text("3546 passed in 44.03s\n", encoding="utf-8")
    stderr.write_text("", encoding="utf-8")
    result = gate.finalize(snapshot, {}, attempt, report, stdout, stderr, 0)
    assert result["status"] == "PASS"
    assert result["pytest_passed_count"] == 3546
    assert result["prior_failure_sha256"] == {}
    assert result["prior_failure_evidence_status"] == "UNAVAILABLE_ORIGINAL_FILES"
    assert report.is_file()
    assert gate.validate_recorded_success(report, snapshot, {})
    with pytest.raises(RuntimeError, match="report exists"):
        gate.finalize(snapshot, {}, attempt, report, stdout, stderr, 0)


def test_preflight_reports_missing_artifacts_as_unverified(tmp_path: Path, monkeypatch, capsys) -> None:
    import sys
    gate = _gate()
    monkeypatch.setattr(gate, "validate_snapshot", lambda repo: {
        "head": gate.REVIEWED_BASE, "remote_head": gate.REVIEWED_BASE,
        "reviewed_blob_count": 15, "repaired_test_count": 3,
        "git_index_tree": "unchanged"
    })
    monkeypatch.setattr(sys, "argv", ["gate", "preflight", "--repo", str(tmp_path),
        "--prior", str(tmp_path / "missing"),
        "--attempt", str(tmp_path / "attempt.json"),
        "--report", str(tmp_path / "report.json"),
        "--allow-missing-prior-evidence"])
    assert gate.main() == 0
    output = capsys.readouterr().out
    assert "PHASE173_FINAL_R2_PRIOR_FAILURE_PRESERVED=NOT_VERIFIABLE" in output
    assert "PHASE173_FINAL_R2_SOURCE_GUARD=PASS" in output
    assert "PHASE173_FINAL_R2_PREFLIGHT=PASS" in output

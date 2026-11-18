"""Fail-closed R4R7 audit contracts; the reports below are synthetic fixtures."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import hashlib
import subprocess

import pytest

from phase175_r4r7_prop25_typed_composition import audit


def passed_r4r6_report() -> dict[str, object]:
    return {
        "phase": "175-R4R6",
        "mode": "READ_ONLY_SOURCE_TYPE_BOUNDARY_AUDIT",
        "gate": audit.PRIOR_GATE,
        "dry_run": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_changes": [],
        "rule_connected_to_public": False,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
        "preflight": {"head": audit.REVIEWED_HEAD},
        "prior_history": {
            "historical_reviewed_head": audit.PRIOR_HISTORICAL_HEAD,
            "historical_production_blob_checked": True,
            "historical_rule_sha256_checked": True,
        },
        "source_evidence": {
            "proposition_2_5_inclusion_and_conditions": True,
            "equation_5_8_signed_identity": True,
            "source_sign_preserved": "±",
            "printed_relation_is_a_verified_proof_step": False,
        },
        "typed_frontier": {
            "m": 4, "i": 8, "j": 9,
            "j_less_than_3m_minus_1": True,
            "typed_endpoints_are_verified_proof_steps": False,
        },
        "order_and_implementation_boundary": {
            "new_prop25_provider_connected": False,
            "signed_reduction_executed_as_proof_step": False,
            "prior_proof_search_executed": False,
        },
    }


def test_r4r6_real_success_shape_validated_without_proof_upgrade() -> None:
    found = audit.validate_prior(passed_r4r6_report())
    assert found["r4r6_head"] == audit.REVIEWED_HEAD
    assert found["printed_source_is_not_proof"] is True
    assert found["r4r6_public_proof_completed"] is False


@pytest.mark.parametrize("name,value", (
    ("phase", "175-R4R5R3"),
    ("gate", audit.DRY_GATE),
    ("dry_run", True),
    ("new_given", 1),
    ("new_mathematical_rules", 1),
    ("production_changes", ["proof.py"]),
    ("rule_connected_to_public", True),
    ("pi95_proof_complete", True),
    ("full_pytest_executed", True),
))
def test_wrong_gate_or_scope_rejected(name: str, value: object) -> None:
    report = passed_r4r6_report()
    report[name] = value
    with pytest.raises(RuntimeError, match="R4R7_R4R6_SCOPE_OR_GATE_INVALID"):
        audit.validate_prior(report)


@pytest.mark.parametrize("section,name,value", (
    ("preflight", "head", "0" * 40),
    ("prior_history", "historical_reviewed_head", "0" * 40),
    ("prior_history", "historical_production_blob_checked", False),
    ("prior_history", "historical_rule_sha256_checked", False),
    ("source_evidence", "equation_5_8_signed_identity", False),
    ("source_evidence", "source_sign_preserved", "+"),
    ("source_evidence", "printed_relation_is_a_verified_proof_step", True),
    ("typed_frontier", "m", 5),
    ("typed_frontier", "j_less_than_3m_minus_1", False),
    ("typed_frontier", "typed_endpoints_are_verified_proof_steps", True),
    ("order_and_implementation_boundary", "new_prop25_provider_connected", True),
    ("order_and_implementation_boundary", "signed_reduction_executed_as_proof_step", True),
    ("order_and_implementation_boundary", "prior_proof_search_executed", True),
))
def test_prior_evidence_change_rejected(section: str, name: str, value: object) -> None:
    report = deepcopy(passed_r4r6_report())
    report[section][name] = value
    with pytest.raises(RuntimeError, match="R4R7_R4R6_EVIDENCE_INVALID"):
        audit.validate_prior(report)


def test_only_latest_valid_real_report_chosen(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    base = tmp_path / "EHPProofTracerAudit" / audit.PRIOR_PACKAGE
    prior = base / "20261117T083246_831773Z"
    later = base / "20261117T083247_831773Z"
    prior.mkdir(parents=True)
    later.mkdir(parents=True)
    (prior / "report.json").write_text(json.dumps(passed_r4r6_report()), encoding="utf-8")
    rejected = passed_r4r6_report()
    rejected["gate"] = "FAIL_R4R6"
    (later / "report.json").write_text(json.dumps(rejected), encoding="utf-8")
    assert audit.latest_real_prior() == prior / "report.json"
    assert audit.latest_real_prior(prior / "report.json") == (prior / "report.json").resolve()
    with pytest.raises(RuntimeError, match="R4R7_R4R6_REPORT_MISSING"):
        audit.latest_real_prior(prior / "missing.json")


def test_missing_or_rejected_reports_fail_closed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    with pytest.raises(RuntimeError, match="R4R7_SUCCESSFUL_R4R6_REPORT_NOT_FOUND"):
        audit.latest_real_prior()
    folder = tmp_path / "EHPProofTracerAudit" / audit.PRIOR_PACKAGE / "20261117"
    folder.mkdir(parents=True)
    (folder / "report.json").write_text('{"gate":"FAIL"}', encoding="utf-8")
    with pytest.raises(RuntimeError, match="R4R7_SUCCESSFUL_R4R6_REPORT_NOT_FOUND"):
        audit.latest_real_prior()


def test_source_guard_rejects_wrong_head(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(audit, "git", lambda root, *args: (
        str(root) if args == ("rev-parse", "--show-toplevel")
        else "develop" if args == ("branch", "--show-current")
        else "0" * 40
    ))
    with pytest.raises(RuntimeError, match="R4R7_UNREVIEWED_HEAD"):
        audit.preflight(tmp_path)


def test_source_guard_rejects_dirty_unrelated_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_git(root: Path, *args: str) -> str:
        if args == ("rev-parse", "--show-toplevel"):
            return str(root)
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return audit.REVIEWED_HEAD
        if args == ("diff", "--name-only"):
            return "proof.py"
        if args == ("diff", "--cached", "--name-only"):
            return ""
        raise AssertionError(args)
    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="R4R7_UNREVIEWED_TRACKED_CHANGES"):
        audit.preflight(tmp_path)


def test_report_is_not_proof_certificate() -> None:
    report = passed_r4r6_report()
    result = audit.validate_prior(report)
    assert "verified_proof_step" not in result
    assert result["printed_source_is_not_proof"] is True


def run_git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True, check=True,
    )
    return result.stdout.strip()


def commit_fixture(root: Path, message: str) -> str:
    run_git(root, "add", ".")
    run_git(root, "-c", "user.name=Test", "-c", "user.email=test@example.com",
            "commit", "-qm", message)
    return run_git(root, "rev-parse", "HEAD")


def synthetic_reviewed_history(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    *, extra_path: str | None = None,
) -> tuple[Path, str, str]:
    """Construct two real Git commits; no synthetic HEAD values are trusted."""
    root = tmp_path / "repo"
    root.mkdir()
    run_git(root, "init", "-q")
    run_git(root, "checkout", "-qb", "develop")
    pinned = root / "proof.py"
    pinned.write_text("reviewed proof source\n", encoding="utf-8")
    old = commit_fixture(root, "reviewed R4R7 base")
    for name in audit.REVIEWED_R4R6_PATHS:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("reviewed R4R6 file: " + name + "\n", encoding="utf-8")
    if extra_path is not None:
        path = root / extra_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("not reviewed\n", encoding="utf-8")
    successor = commit_fixture(root, "175-4-6")
    monkeypatch.setattr(audit, "REVIEWED_HEAD", old)
    monkeypatch.setattr(audit, "REVIEWED_R4R6_HEAD", successor)
    monkeypatch.setattr(audit, "PINNED_GIT_BLOBS", {
        "proof.py": run_git(root, "rev-parse", "HEAD:proof.py"),
    })
    sha = hashlib.sha256((root / audit.PRIOR_PACKAGE / "audit.py").read_bytes()).hexdigest()
    monkeypatch.setattr(audit, "PRIOR_AUDIT_SHA256", sha)
    return root, old, successor


def test_reviewed_r4r6_successor_with_exact_paths_accepted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, old, successor = synthetic_reviewed_history(tmp_path, monkeypatch)
    result = audit.preflight(root)
    assert result["head"] == successor
    assert result["reviewed_r4r7_base_head"] == old
    assert result["reviewed_intervening_paths"] == sorted(audit.REVIEWED_R4R6_PATHS)
    assert result["pinned_blobs"] == 1


def test_unreviewed_extra_file_in_r4r6_commit_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, _, _ = synthetic_reviewed_history(
        tmp_path, monkeypatch, extra_path="unreviewed_source.py",
    )
    with pytest.raises(RuntimeError, match="R4R7_UNREVIEWED_R4R6_LINEAGE"):
        audit.preflight(root)


def test_later_unreviewed_head_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, _, _ = synthetic_reviewed_history(tmp_path, monkeypatch)
    (root / "new_file.txt").write_text("later commit\n", encoding="utf-8")
    next_head = commit_fixture(root, "unaudited later commit")
    with pytest.raises(RuntimeError, match="R4R7_UNREVIEWED_HEAD: " + next_head):
        audit.preflight(root)


def test_reviewed_successor_source_blob_drift_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, _, _ = synthetic_reviewed_history(tmp_path, monkeypatch)
    monkeypatch.setattr(audit, "PINNED_GIT_BLOBS", {"proof.py": "0" * 40})
    with pytest.raises(RuntimeError, match="R4R7_SOURCE_BLOB_DRIFT"):
        audit.preflight(root)


def test_reviewed_successor_r4r6_audit_bytes_drift_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, _, _ = synthetic_reviewed_history(tmp_path, monkeypatch)
    audit_file = root / audit.PRIOR_PACKAGE / "audit.py"
    audit_file.write_text("modified source\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="R4R7_UNREVIEWED_TRACKED_CHANGES"):
        audit.preflight(root)
    run_git(root, "restore", "--", audit.PRIOR_PACKAGE + "/audit.py")
    monkeypatch.setattr(audit, "PRIOR_AUDIT_SHA256", "0" * 64)
    with pytest.raises(RuntimeError, match="R4R7_REVIEWED_R4R6_AUDIT_DRIFT"):
        audit.preflight(root)


def test_wrong_ancestry_in_reviewed_successor_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, _, _ = synthetic_reviewed_history(tmp_path, monkeypatch)
    monkeypatch.setattr(audit, "REVIEWED_HEAD", "0" * 40)
    with pytest.raises(RuntimeError, match="R4R7_GIT_ERROR"):
        audit.preflight(root)

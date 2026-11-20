"""Focused, read-only audit contract tests."""
from __future__ import annotations

import json

import pytest

from phase176_r3r2_finite_cyclic_hopf_frontier import audit


def test_proposals_are_not_proof_steps() -> None:
    class FakeRule:
        name = "test only"

    class FakeExpansion:
        rule = FakeRule()
        subgoals = ("unfinished",)

    record = audit.proposal_summary("goal", lambda goal: (FakeExpansion(),))
    assert record["status"] == "INSPECTED_NOT_PROVED"
    assert record["count"] == 1
    assert record["rules"] == ["test only"]
    assert record["subgoals"][0][0]["repr"] == "'unfinished'"


def test_provider_error_is_not_silenced() -> None:
    def broken(goal: object) -> tuple:
        raise ValueError("test failure")

    record = audit.proposal_summary("goal", broken)
    assert record["status"] == "ERROR"
    assert "ValueError" in record["error"]


def test_dryrun_never_invokes_worker(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setattr(audit, "preflight", lambda: {"head": "sample"})
    monkeypatch.setattr(audit, "worker", lambda timeout: pytest.fail("worker started"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.run(True, 5) == 0
    saved = json.loads((tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json").read_text(encoding="utf-8"))
    assert saved["gate"] == "PASS_R3R2_READ_ONLY_DRYRUN"
    assert saved["full_pytest"] == "NOT_RUN"


def test_preflight_rejects_dirty_checkout(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    for name in audit.REQUIRED_FILES:
        p = tmp_path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("fixture", encoding="utf-8")

    def fake_git(*args: str, check: bool = True) -> tuple[int, str]:
        if args[0] == "rev-parse" and args[1] == "--show-toplevel":
            return 0, str(tmp_path)
        if args[0] == "branch":
            return 0, "develop"
        if args[0] == "merge-base":
            return 0, ""
        if args[0] == "status":
            return 0, " M source.py"
        return 0, "head"

    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="TRACKED_CHANGES_REQUIRE_REVIEW"):
        audit.preflight()


def test_worker_does_not_accept_proof_claim(monkeypatch: pytest.MonkeyPatch) -> None:
    class Proc:
        returncode = 0
        stderr = ""
        stdout = audit.MARKER + '{"proof_complete": true}'

    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **k: Proc())
    with pytest.raises(RuntimeError, match="AUDIT_NOT_ALLOWED_TO_CLAIM_PROOF"):
        audit.worker(5)

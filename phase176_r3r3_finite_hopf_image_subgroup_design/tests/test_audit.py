"""Focused non-production R3R3 audit tests."""
from __future__ import annotations

import json

import pytest

from phase176_r3r3_finite_hopf_image_subgroup_design import audit


def test_old_lift_guard_accepts_only_equal_order() -> None:
    assert audit.classify_codomain_order(2, 2) == "OLD_RULE_ORDER_GUARD_ACCEPTS"
    assert audit.classify_codomain_order(2, 8) == "OLD_RULE_ORDER_GUARD_REJECTS"


def test_order_classifier_refuses_invalid_data() -> None:
    assert audit.classify_codomain_order(True, 8) == "INVALID_GOAL_ORDER"
    assert audit.classify_codomain_order(2, None) == "CODOMAIN_ORDER_UNKNOWN"


def test_expansion_is_not_labeled_as_proof() -> None:
    class Rule:
        name = "hypothetical test"

    class Proposal:
        rule = Rule()
        subgoals = ("not yet proved",)

    row = audit.describe_options(lambda goal: (Proposal(),), "request")
    assert row["status"] == "PROPOSALS_NOT_PROOFS"
    assert row["count"] == 1
    assert row["premises"][0][0]["repr"] == "'not yet proved'"


def test_proposal_exception_visible() -> None:
    def broken(goal):
        raise ValueError("not grounded")

    row = audit.describe_options(broken, object())
    assert row["status"] == "PROVIDER_ERROR"
    assert "ValueError" in row["error"]


def test_preflight_fails_closed_on_dirty_tracked_file(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    for name in audit.SOURCES:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture", encoding="utf-8")

    def fake_git(*args, check=True):
        key = args[0]
        if key == "rev-parse" and args[1] == "--show-toplevel":
            return 0, str(tmp_path)
        if key == "branch":
            return 0, "develop"
        if key == "merge-base":
            return 0, ""
        if key == "status":
            return 0, " M source.py"
        return 0, "head"

    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="TRACKED_CHANGES_REQUIRE_REVIEW"):
        audit.preflight()


def test_dry_run_does_not_start_worker(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setattr(audit, "preflight", lambda: {"head": "test-head"})
    monkeypatch.setattr(audit, "worker", lambda timeout: pytest.fail("worker started"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.run(True, 5) == 0
    path = tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json"
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert saved["gate"] == "PASS_R3R3_READ_ONLY_DRYRUN"
    assert saved["proof_complete"] is False
    assert saved["full_pytest"] == "NOT_RUN"


def test_worker_rejects_false_proof_claim(monkeypatch: pytest.MonkeyPatch) -> None:
    class Process:
        returncode = 0
        stderr = ""
        stdout = audit.MARKER + '{"proof_complete":true,"new_given":0}'

    monkeypatch.setattr(audit.subprocess, "run", lambda *args, **kwargs: Process())
    with pytest.raises(RuntimeError, match="R3R3_AUDIT_CANNOT_CLAIM_PROOF"):
        audit.worker(5)

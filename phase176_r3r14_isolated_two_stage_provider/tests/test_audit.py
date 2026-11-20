"""Focused fail-closed audit and dry-run contracts."""
from __future__ import annotations

import json

import pytest

from phase176_r3r14_isolated_two_stage_provider import audit


def test_dry_run_does_not_launch_worker(monkeypatch, tmp_path):
    monkeypatch.setattr(audit, "preflight", lambda: {"head": "fixture", "source_anchors": 5})
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(True, 5) == 0
    report = json.loads((tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json").read_text(encoding="utf-8"))
    assert report["gate"] == "PASS_R3R14_READ_ONLY_DRYRUN"
    assert "observed" not in report
    assert report["root_proof_complete"] is False


def test_failed_preflight_does_not_claim_success(monkeypatch, tmp_path):
    def fail():
        raise RuntimeError("GUARD_FAILED")
    monkeypatch.setattr(audit, "preflight", fail)
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(True, 5) == 1
    report = json.loads((tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json").read_text(encoding="utf-8"))
    assert report["gate"] == "FAIL_R3R14"
    assert "GUARD_FAILED" in report["error"]

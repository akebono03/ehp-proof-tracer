"""Focused, isolated Phase 176 R3R17 contracts."""
from __future__ import annotations

import json

import pytest

from phase176_r3r17_root_frontier_audit import audit


def test_empty_root_options_after_proved_zero_image_is_not_complete() -> None:
    assert audit.classify_frontier(
        public_status="search_failed", root_options_count=0,
        proved_zero_image=True,
    ) == "ROOT_RULE_FRONTIER_AFTER_PROVED_ZERO_IMAGE"


def test_root_candidates_stay_unverified() -> None:
    class Rule:
        name = "example"

    class Option:
        rule = Rule()
        subgoals = ("independent premise",)

    summary = audit.describe_options((Option(),))
    assert summary["count"] == 1
    assert summary["options"][0]["subgoals"] == ["'independent premise'"]
    assert audit.classify_frontier(
        public_status="search_failed", root_options_count=1,
        proved_zero_image=True,
    ) == "ROOT_HAS_UNVERIFIED_CANDIDATES"


def test_dryrun_does_not_execute_observation(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(audit, "preflight", lambda: {"head": "test"})
    monkeypatch.setattr(audit, "observe", lambda: pytest.fail("worker ran"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(True) == 0
    data = json.loads((tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json").read_text(encoding="utf-8"))
    assert data["gate"] == "PASS_R3R17_READ_ONLY_DRYRUN"
    assert "observed" not in data
    assert data["full_pytest"] == "NOT_RUN"


def test_failed_observation_fails_closed(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(audit, "preflight", lambda: {"head": "test"})
    monkeypatch.setattr(audit, "observe", lambda: (_ for _ in ()).throw(RuntimeError("blocked")))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(False) == 1
    data = json.loads((tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json").read_text(encoding="utf-8"))
    assert data["gate"] == "FAIL_R3R17"
    assert "blocked" in data["error"]

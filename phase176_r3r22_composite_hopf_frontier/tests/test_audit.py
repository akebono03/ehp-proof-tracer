"""Focused tests for read-only composite-left Hopf audit."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from phase176_r3r22_composite_hopf_frontier import audit


def test_source_guard_requires_all_sources(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="SOURCE_MISSING"):
        audit.inspect_source(tmp_path)


def test_dry_run_never_probes(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    monkeypatch.setattr(audit, "checked_git_root", lambda root: "test-head")
    monkeypatch.setattr(audit, "inspect_source", lambda root: {"ok": True})
    monkeypatch.setattr(audit, "probe", lambda: pytest.fail("probe called on dry run"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(True) == 0
    report = json.loads((tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json").read_text(encoding="utf-8"))
    assert report["gate"] == "PASS_R3R22_DRYRUN"
    assert "observed" not in report


def test_probe_failure_fails_closed(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "checked_git_root", lambda root: "test-head")
    monkeypatch.setattr(audit, "inspect_source", lambda root: {"ok": True})
    monkeypatch.setattr(audit, "probe", lambda: (_ for _ in ()).throw(RuntimeError("probe_failed")))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(False) == 1
    report = json.loads((tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json").read_text(encoding="utf-8"))
    assert report["gate"] == "FAIL_R3R22"
    assert "probe_failed" in report["error"]


def test_actual_composite_left_boundary() -> None:
    observed = audit.probe()
    assert observed["left_factor_is_composition"]
    assert observed["left_factor_mathematically_composable"]
    assert observed["candidate_is_proof"] is False
    assert observed["new_given"] == 0
    assert observed["new_math_rules"] == 0

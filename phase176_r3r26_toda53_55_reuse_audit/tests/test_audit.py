"""Focused fail-closed contracts for R3R26 read-only audit."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase176_r3r26_toda53_55_reuse_audit import audit


def test_source_guard_rejects_empty_tree(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="SOURCE_ANCHOR_MISSING"):
        audit.verify_sources(tmp_path)


def test_dryrun_skips_live_capture(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    monkeypatch.setattr(audit, "verify_checkout", lambda root: {"head": "test-head", "modified_files": ()})
    monkeypatch.setattr(audit, "verify_sources", lambda root: {"checked": True})
    monkeypatch.setattr(audit, "audit_live", lambda: pytest.fail("unexpected live capture"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(True) == 0
    p = tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["gate"] == "PASS_R3R26_DRYRUN"
    assert "observed" not in data


def test_live_failure_fails_closed(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    monkeypatch.setattr(audit, "verify_checkout", lambda root: {"head": "test-head"})
    monkeypatch.setattr(audit, "verify_sources", lambda root: {"checked": True})
    monkeypatch.setattr(audit, "audit_live", lambda: (_ for _ in ()).throw(RuntimeError("forced_failure")))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(False) == 1
    p = tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["gate"] == "FAIL_R3R26"
    assert "forced_failure" in data["error"]

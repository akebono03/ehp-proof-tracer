"""Isolated tests for Phase 176 R3R20 audit mechanics."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase176_r3r20_cyclic_candidate_boundary import audit


def test_source_guard_requires_all_anchors(tmp_path: Path) -> None:
    for name in audit.REQUIRED:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
    with pytest.raises(RuntimeError, match="SOURCE_ANCHOR_MISSING"):
        audit.inspect_source(tmp_path)


def test_dry_run_does_not_capture(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    monkeypatch.setattr(audit, "checked_git_root", lambda root: "test-head")
    monkeypatch.setattr(audit, "inspect_source", lambda root: {"test": True})
    monkeypatch.setattr(audit, "capture", lambda: pytest.fail("unexpected capture"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(True) == 0
    path = tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json"
    report = json.loads(path.read_text(encoding="utf-8"))
    assert report["gate"] == "PASS_R3R20_READ_ONLY_DRYRUN"
    assert "observed" not in report


def test_capture_failure_fails_closed(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "checked_git_root", lambda root: "test-head")
    monkeypatch.setattr(audit, "inspect_source", lambda root: {"test": True})
    monkeypatch.setattr(audit, "capture", lambda: (_ for _ in ()).throw(RuntimeError("probe_failed")))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(False) == 1
    report = json.loads((tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json").read_text(encoding="utf-8"))
    assert report["gate"] == "FAIL_R3R20"
    assert "probe_failed" in report["error"]

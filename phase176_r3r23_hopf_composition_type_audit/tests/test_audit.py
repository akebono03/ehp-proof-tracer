"""Focused read-only guard tests for R3R23."""
from pathlib import Path
import json
import pytest
from phase176_r3r23_hopf_composition_type_audit import audit


def test_missing_source_fails_closed(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="SOURCE_ANCHOR_MISSING"):
        audit.inspect_source(tmp_path)


def test_dry_run_never_calls_runtime(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    monkeypatch.setattr(audit, "git_state", lambda root: {"head": "test", "branch": "develop"})
    monkeypatch.setattr(audit, "inspect_source", lambda root: {"verified": True})
    monkeypatch.setattr(audit, "inspect_runtime", lambda: pytest.fail("runtime invoked"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(True) == 0
    data = json.loads(audit.report_path().read_text(encoding="utf-8"))
    assert data["gate"] == "PASS_R3R23_DRYRUN"
    assert "observed" not in data


def test_runtime_error_fails_closed(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    monkeypatch.setattr(audit, "git_state", lambda root: {"head": "test", "branch": "develop"})
    monkeypatch.setattr(audit, "inspect_source", lambda root: {"verified": True})
    monkeypatch.setattr(audit, "inspect_runtime", lambda: (_ for _ in ()).throw(RuntimeError("probe_failure")))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(False) == 1
    data = json.loads(audit.report_path().read_text(encoding="utf-8"))
    assert "probe_failure" in data["error"]

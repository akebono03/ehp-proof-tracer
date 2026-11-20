"""Focused failure-boundary contracts for Phase 176 R3R29."""
from pathlib import Path

import pytest

from phase176_r3r29_hopf_right_connection_audit import audit


def test_missing_source_fails_closed(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="MISSING_SOURCE"):
        audit.source_guard(tmp_path)


def test_source_signature_fails_closed(tmp_path: Path) -> None:
    for filename, anchors in audit.ANCHORS.items():
        path = tmp_path / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(anchors), encoding="utf-8")
    assert all(audit.source_guard(tmp_path).values())
    item = tmp_path / next(iter(audit.ANCHORS))
    item.write_text("modified", encoding="utf-8")
    with pytest.raises(RuntimeError, match="SOURCE_SIGNATURE_CHANGED"):
        audit.source_guard(tmp_path)


def test_dryrun_never_invokes_probe(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    monkeypatch.setattr(audit, "preflight", lambda root: "test-head")
    monkeypatch.setattr(audit, "source_guard", lambda root: {"ok": True})
    monkeypatch.setattr(audit, "probe", lambda: pytest.fail("probe should not run"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.run(True) == 0


def test_probe_exception_cannot_claim_pass(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    monkeypatch.setattr(audit, "preflight", lambda root: "test-head")
    monkeypatch.setattr(audit, "source_guard", lambda root: {"ok": True})
    monkeypatch.setattr(audit, "probe", lambda: (_ for _ in ()).throw(RuntimeError("blocked")))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.run(False) == 1

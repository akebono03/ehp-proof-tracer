"""Offline-focused protection tests; no production imports or Git writes."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from phase173_r4_r1_source_bound_56 import audit


def test_preflight_accepts_only_exact_reviewed_blobs(monkeypatch, tmp_path: Path) -> None:
    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return "audit-only-new-head"
        if len(args) == 2 and args[0] == "rev-parse" and args[1].startswith("HEAD:"):
            return audit.REVIEWED_BLOBS[args[1][5:]]
        raise AssertionError(args)

    monkeypatch.setattr(audit, "_git", fake_git)
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=0))
    result = audit.preflight(tmp_path)
    assert result["head"] == "audit-only-new-head"
    assert len(result["verified_files"]) == len(audit.REVIEWED_BLOBS)


def test_preflight_rejects_modified_source_blob(monkeypatch, tmp_path: Path) -> None:
    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return "audit-only-new-head"
        if args == ("rev-parse", "HEAD:sources/toda/Toda_05_2.tex"):
            return "tampered"
        if len(args) == 2 and args[0] == "rev-parse" and args[1].startswith("HEAD:"):
            return audit.REVIEWED_BLOBS[args[1][5:]]
        raise AssertionError(args)

    monkeypatch.setattr(audit, "_git", fake_git)
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=0))
    with pytest.raises(RuntimeError, match="Reviewed production blob changed"):
        audit.preflight(tmp_path)


def test_preflight_rejects_modified_worktree_source(monkeypatch, tmp_path: Path) -> None:
    def fake_git(root: Path, *args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return "audit-only-new-head"
        if len(args) == 2 and args[0] == "rev-parse" and args[1].startswith("HEAD:"):
            return audit.REVIEWED_BLOBS[args[1][5:]]
        raise AssertionError(args)

    monkeypatch.setattr(audit, "_git", fake_git)
    monkeypatch.setattr(audit.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=1))
    with pytest.raises(RuntimeError, match="production working file changed"):
        audit.preflight(tmp_path)


def test_preflight_rejects_wrong_branch(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "_git", lambda *a: "main")
    with pytest.raises(RuntimeError, match="develop"):
        audit.preflight(tmp_path)


def test_reviewed_manifest_contains_original_source_and_provider() -> None:
    assert "sources/toda/Toda_04_2.tex" in audit.REVIEWED_BLOBS
    assert "phase165_r52_r9_shared_math.py" in audit.REVIEWED_BLOBS
    assert "toda_rules.py" in audit.REVIEWED_BLOBS

"""Focused audit guards; production-backed run is executed by audit.py."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from phase175_r4r14_pi106_frontier_audit import audit


def test_target_is_pi106() -> None:
    assert audit.TARGET == (6, 4)
    assert len(audit.ROOT_FILES) == 6


def test_source_guard_rejects_wrong_repository(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "git", lambda root, *args: str(tmp_path / "elsewhere"))
    with pytest.raises(RuntimeError, match="WRONG_REPOSITORY_ROOT"):
        audit.source_guard(tmp_path)


def test_source_guard_rejects_branch_change(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    def fake_git(root: Path, *args: str) -> str:
        if args == ("rev-parse", "--show-toplevel"):
            return str(tmp_path)
        if args == ("branch", "--show-current"):
            return "main"
        return ""
    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="EXPECTED_DEVELOP"):
        audit.source_guard(tmp_path)


def test_audit_failure_is_fail_closed(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "source_guard", lambda root: (_ for _ in ()).throw(RuntimeError("NO_SOURCE")))
    monkeypatch.setenv("TEMP", str(tmp_path))
    assert audit.run(tmp_path, dry_run=True) == 1
    assert (tmp_path / "EHP_Phase175_R4R14_pi106_frontier.json").is_file()

"""Focused tests of R15R1 HEAD lineage and content guards."""
from __future__ import annotations

from pathlib import Path
import subprocess

import pytest

from phase173_r4_r15r2_generator_obligation_audit import preflight as guard


def _git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ("git", *args), cwd=root, capture_output=True, text=True, check=True,
    )
    return completed.stdout.strip()


def _make_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, str, str]:
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-b", "develop")
    _git(root, "config", "user.name", "Test User")
    _git(root, "config", "user.email", "tester@example.invalid")
    core_file = root / guard.TARGET
    core_file.parent.mkdir(parents=True)
    core_file.write_bytes(b"original\n")
    _git(root, "add", "--", guard.TARGET)
    _git(root, "commit", "-m", "reviewed original")
    old_head = _git(root, "rev-parse", "HEAD")
    original_blob = _git(root, "rev-parse", "HEAD:" + guard.TARGET)

    patch_file = root / guard.PATCH_SOURCE
    patch_file.parent.mkdir(parents=True)
    patch_file.write_bytes(b"reviewed patch implementation\n")
    core_file.write_bytes(b"installed R15R1\n")
    _git(root, "add", "--", guard.TARGET, guard.PATCH_SOURCE)
    _git(root, "commit", "-m", "reviewed R15R1")
    new_head = _git(root, "rev-parse", "HEAD")
    monkeypatch.setattr(guard, "REVIEWED_HEAD", old_head)
    monkeypatch.setattr(guard, "REVIEWED_R15R1_COMMITTED_HEAD", new_head)
    monkeypatch.setattr(guard, "ORIGINAL_BLOB", original_blob)
    monkeypatch.setattr(guard, "REVIEWED_COMMITTED_CORE_BLOB", _git(root, "rev-parse", "HEAD:" + guard.TARGET))
    monkeypatch.setattr(guard, "REVIEWED_COMMITTED_PATCH_BLOB", _git(root, "rev-parse", "HEAD:" + guard.PATCH_SOURCE))
    monkeypatch.setattr(guard, "transform", lambda source: b"installed R15R1\n" if source == b"original\n" else b"unexpected\n")
    return root, old_head, new_head


def test_accepts_reviewed_committed_r15r1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root, _, new_head = _make_repo(tmp_path, monkeypatch)
    assert guard.reviewed_installed_core(root, new_head) == "COMMITTED_PATCH"


def test_accepts_reviewed_local_r15r1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root, old_head, _ = _make_repo(tmp_path, monkeypatch)
    _git(root, "checkout", old_head)
    (root / guard.TARGET).write_bytes(b"installed R15R1\n")
    assert guard.reviewed_installed_core(root, old_head) == "LOCAL_PATCH"


def test_rejects_unreviewed_future_commit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root, _, _ = _make_repo(tmp_path, monkeypatch)
    _git(root, "commit", "--allow-empty", "-m", "unreviewed successor")
    with pytest.raises(RuntimeError, match="Unreviewed R15R1 commit lineage"):
        guard.reviewed_installed_core(root, _git(root, "rev-parse", "HEAD"))


def test_rejects_modified_worktree_core(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root, _, new_head = _make_repo(tmp_path, monkeypatch)
    (root / guard.TARGET).write_bytes(b"changed\n")
    with pytest.raises(RuntimeError, match="does not equal reviewed transformation"):
        guard.reviewed_installed_core(root, new_head)


def test_rejects_modified_worktree_patch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root, _, new_head = _make_repo(tmp_path, monkeypatch)
    (root / guard.PATCH_SOURCE).write_bytes(b"unreviewed patch implementation\n")
    with pytest.raises(RuntimeError, match="Unreviewed local R15R1 patch implementation"):
        guard.reviewed_installed_core(root, new_head)


def test_rejects_committed_core_with_wrong_blob(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root, _, new_head = _make_repo(tmp_path, monkeypatch)
    monkeypatch.setattr(guard, "REVIEWED_COMMITTED_CORE_BLOB", "0" * 40)
    with pytest.raises(RuntimeError, match="Committed R15R1 core blob changed"):
        guard.reviewed_installed_core(root, new_head)

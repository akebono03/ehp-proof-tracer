"""Focused real-Git safety tests. They never touch the user's repository."""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from phase169_git_environment_r2_preserve_and_quarantine.recover import (
    CONFLICT_PATHS,
    backup_and_quarantine,
    conflict_paths,
    preflight,
    sha256,
)


def local_git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True, capture_output=True, text=True, encoding="utf-8",
    )
    return proc.stdout.strip()


def make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "workspace"
    repo.mkdir()
    local_git(repo, "init", "--quiet")
    local_git(repo, "symbolic-ref", "HEAD", "refs/heads/develop")
    (repo / "tracked.py").write_text("version=1\n", encoding="utf-8")
    local_git(repo, "add", "tracked.py")
    local_git(repo, "-c", "user.name=Safety Test", "-c", "user.email=safety@example.invalid",
              "commit", "-m", "initial", "--quiet")
    local_git(repo, "update-ref", "refs/remotes/origin/develop", "HEAD")
    for path in CONFLICT_PATHS:
        file = repo / ".git" / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("Dropbox copy\n", encoding="utf-8")
    return repo


def test_audit_only_validates_conflict_set_without_changes(tmp_path: Path):
    repo = make_repo(tmp_path)
    original = {p: sha256(repo / ".git" / p) for p in CONFLICT_PATHS}
    result = preflight(repo, tmp_path / "recover_out", "audit", False)
    assert result["branch"] == "refs/heads/develop"
    assert set(result["conflict_paths"]) == set(CONFLICT_PATHS)
    assert original == {p: sha256(repo / ".git" / p) for p in CONFLICT_PATHS}


def test_quarantine_refuses_without_sync_confirmation(tmp_path: Path):
    repo = make_repo(tmp_path)
    with pytest.raises(RuntimeError, match="DropboxPaused"):
        preflight(repo, tmp_path / "recover_out", "quarantine", False)
    assert len(conflict_paths(repo)) == 3


def test_unrecognized_conflict_copy_refuses_quarantine(tmp_path: Path):
    repo = make_repo(tmp_path)
    extra = repo / ".git" / "refs" / "heads" / "main (conflicted copy)"
    extra.write_text("not a valid reference\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Unexpected conflict-copy set"):
        preflight(repo, tmp_path / "recover_out", "quarantine", True)
    assert extra.exists()


def test_real_quarantine_keeps_head_index_and_worktree(tmp_path: Path):
    repo = make_repo(tmp_path)
    original_head = local_git(repo, "rev-parse", "HEAD")
    (repo / "tracked.py").write_text("version=2\n", encoding="utf-8")
    original_bytes = (repo / "tracked.py").read_bytes()
    audit = repo / "audit" / "README.md"
    audit.parent.mkdir(parents=True)
    audit.write_text("Staged audit evidence\n", encoding="utf-8")
    local_git(repo, "add", "audit/README.md")
    index_hash = sha256(repo / ".git" / "index")
    pre = preflight(repo, tmp_path / "recover_out", "quarantine", True)
    target = backup_and_quarantine(repo, tmp_path / "recover_out", pre)
    assert conflict_paths(repo) == ()
    assert all((target / "quarantined_git_files" / p).is_file() for p in CONFLICT_PATHS)
    assert all((target / "git_complete_backup" / p).is_file() for p in CONFLICT_PATHS)
    assert sha256(repo / ".git" / "index") == index_hash
    assert local_git(repo, "rev-parse", "HEAD") == original_head
    assert (repo / "tracked.py").read_bytes() == original_bytes
    assert (target / "tracked_worktree_backup" / "tracked.py").read_bytes() == original_bytes
    assert (target / "tracked_worktree_backup" / "audit" / "README.md").is_file()
    assert "audit/README.md" in local_git(repo, "diff", "--cached", "--name-only")


def test_backup_location_must_be_outside_repository_and_dropbox(tmp_path: Path):
    repo = make_repo(tmp_path)
    with pytest.raises(RuntimeError, match="separate"):
        preflight(repo, repo / "quarantine", "audit", False)
    with pytest.raises(RuntimeError, match="OUTSIDE Dropbox"):
        preflight(repo, tmp_path / "Dropbox" / "backup", "audit", False)

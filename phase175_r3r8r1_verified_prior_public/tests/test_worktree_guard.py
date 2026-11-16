"""Real-Git tests for the successor-only tracked-file exception."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import subprocess

import pytest

from phase175_r3_pi73_hopf_lift import audit as r3
from phase175_r3r8r1_verified_prior_public.worktree_guard import (
    PUBLIC_TARGET,
    REVIEWED_SUCCESSOR_WORKTREE_FILES,
    reviewed_tracked_snapshot,
)


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    assert completed.returncode == 0, completed.stderr
    return completed.stdout.strip()


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q")
    for name in (
        PUBLIC_TARGET,
        "phase175_r3r8r1_verified_prior_public/AUDIT_PLAN_JA.md",
        "phase175_r3r8r1_verified_prior_public/audit.py",
        "phase175_r3_pi73_hopf_lift/README.md",
        "production_other.py",
    ):
        file = root / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("reviewed baseline\n", encoding="utf-8")
    git(root, "add", "-A")
    git(root, "-c", "user.name=EHP Audit Test",
        "-c", "user.email=test@example.invalid", "commit", "-q", "-m", "baseline")
    return root


@pytest.mark.parametrize("name", (
    "phase175_r3r8r1_verified_prior_public/AUDIT_PLAN_JA.md",
    "phase175_r3r8r1_verified_prior_public/audit.py",
    "phase175_r3_pi73_hopf_lift/README.md",
))
def test_named_unstaged_audit_change_is_hashed(repo: Path, name: str) -> None:
    (repo / name).write_text("reviewed replacement\n", encoding="utf-8")
    snapshot = reviewed_tracked_snapshot(repo)
    assert snapshot == {
        name: sha256((repo / name).read_bytes()).hexdigest(),
    }


def test_reviewed_successor_filename_whitelist_is_explicit() -> None:
    assert "phase175_r3r8r1_verified_prior_public/audit.py" in REVIEWED_SUCCESSOR_WORKTREE_FILES
    assert PUBLIC_TARGET not in REVIEWED_SUCCESSOR_WORKTREE_FILES
    assert "production_other.py" not in REVIEWED_SUCCESSOR_WORKTREE_FILES
    assert not any(name.endswith("/*") for name in REVIEWED_SUCCESSOR_WORKTREE_FILES)
    assert "phase175_r3_pi73_hopf_lift/README.md" in r3.R3_ALLOWED_TRACKED_EDITS


@pytest.mark.parametrize("name", (PUBLIC_TARGET, "production_other.py"))
def test_production_modifications_are_rejected_before_install(repo: Path, name: str) -> None:
    (repo / name).write_text("unauthorized modification\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="R3R8R1R2_PROTECTED_TRACKED_CHANGE"):
        reviewed_tracked_snapshot(repo)


def test_public_target_only_allowed_after_patch(repo: Path) -> None:
    name = "phase175_r3r8r1_verified_prior_public/AUDIT_PLAN_JA.md"
    (repo / name).write_text("reviewed replacement\n", encoding="utf-8")
    prior = reviewed_tracked_snapshot(repo)
    (repo / PUBLIC_TARGET).write_text("exact public patch fixture\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="R3R8R1R2_PROTECTED_TRACKED_CHANGE"):
        reviewed_tracked_snapshot(repo)
    actual = reviewed_tracked_snapshot(repo, allow_public_target=True)
    assert actual.pop(PUBLIC_TARGET) == sha256((repo / PUBLIC_TARGET).read_bytes()).hexdigest()
    assert actual == prior


def test_untracked_successor_files_do_not_override_old_policy(repo: Path) -> None:
    new = repo / "phase175_r3r8r1_verified_prior_public/worktree_guard.py"
    new.write_text("new audited file\n", encoding="utf-8")
    assert reviewed_tracked_snapshot(repo) == {}


def test_unlisted_successor_tracking_is_rejected(repo: Path) -> None:
    new = repo / "phase175_r3r8r1_verified_prior_public/unknown.py"
    new.write_text("unreviewed\n", encoding="utf-8")
    git(repo, "add", "-N", str(new.relative_to(repo)))
    with pytest.raises(RuntimeError, match="R3R8R1R2_STAGED_OR_OTHER_TRACKED_CHANGE"):
        reviewed_tracked_snapshot(repo)


def test_staged_reviewed_edit_rejected(repo: Path) -> None:
    name = "phase175_r3r8r1_verified_prior_public/AUDIT_PLAN_JA.md"
    (repo / name).write_text("staged replacement\n", encoding="utf-8")
    git(repo, "add", name)
    with pytest.raises(RuntimeError, match="R3R8R1R2_STAGED_OR_OTHER_TRACKED_CHANGE"):
        reviewed_tracked_snapshot(repo)


def test_dirty_production_cannot_be_hidden_by_a_reviewed_change(repo: Path) -> None:
    doc = repo / "phase175_r3r8r1_verified_prior_public/AUDIT_PLAN_JA.md"
    doc.write_text("reviewed replacement\n", encoding="utf-8")
    (repo / "production_other.py").write_text("unreviewed\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="R3R8R1R2_PROTECTED_TRACKED_CHANGE"):
        reviewed_tracked_snapshot(repo)


def test_installer_accepts_reviewed_dirty_docs_and_preserves_them(
    repo: Path, monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    from phase175_r3r8r1_verified_prior_public import install

    git(repo, "branch", "-m", "develop")
    template = (install.PACKAGE / "search_shared_group_goal_FULL.py.txt").read_text(
        encoding="utf-8",
    )
    original = template.replace(install.PUBLIC_INSERTION, "")
    (repo / PUBLIC_TARGET).write_text(original, encoding="utf-8")
    git(repo, "add", PUBLIC_TARGET)
    git(repo, "-c", "user.name=EHP Audit Test",
        "-c", "user.email=test@example.invalid", "commit", "-q", "-m", "source fixture")
    committed_blob = git(repo, "rev-parse", "HEAD:" + PUBLIC_TARGET)
    monkeypatch.setattr(install, "PINNED_GIT_BLOB", committed_blob)

    doc = repo / "phase175_r3r8r1_verified_prior_public/AUDIT_PLAN_JA.md"
    doc.write_text("reviewed replacement\n", encoding="utf-8")
    before_doc = reviewed_tracked_snapshot(repo)
    assert set(before_doc) == {str(doc.relative_to(repo)).replace("\\", "/")}

    evidence = install.preflight(repo)
    assert evidence["reviewed_tracked_before"] == before_doc
    backup_dir = tmp_path / "backup"
    installed = install.apply(repo, backup_dir)
    install.verify_postflight(repo, installed)
    assert (repo / PUBLIC_TARGET).read_text(encoding="utf-8") != original
    install.rollback(repo, backup_dir)
    assert (repo / PUBLIC_TARGET).read_text(encoding="utf-8") == original
    assert reviewed_tracked_snapshot(repo) == before_doc

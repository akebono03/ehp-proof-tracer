"""Regression tests for Phase 175 successor lineage without weakening R3R7."""
from __future__ import annotations

from pathlib import Path
import subprocess

import pytest

from phase175_r3r8r1_verified_prior_public import audit


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def commit(root: Path, message: str) -> str:
    git(root, "add", "-A")
    git(root, "-c", "user.name=EHP Audit Test",
        "-c", "user.email=test@example.invalid", "commit", "-q", "-m", message)
    return git(root, "rev-parse", "HEAD")


@pytest.fixture
def repo(tmp_path: Path):
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q")
    (root / "baseline.py").write_text("production = 1\n", encoding="utf-8")
    start = commit(root, "source baseline")
    return root, start


@pytest.mark.parametrize("path", [
    "phase175_r3r8_pi73_public_connection/AUDIT_PLAN_JA.md",
    "phase175_r3r8_pi73_public_connection/route.py",
    "phase175_r3r8r1_verified_prior_public/rule.py",
    "phase175_r3r8r1_verified_prior_public/worktree_guard.py",
    "phase175_r3r7_lemma54_membership/audit.py",
])
def test_reviewed_additive_successor_accepted(repo, path: str) -> None:
    root, start = repo
    file_path = root / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("reviewed package file\n", encoding="utf-8")
    end = commit(root, "reviewed package addition")
    result = audit.verify_extended_lineage(
        root, {"preflight": {"head": start}}, {"head": end},
    )
    assert result["audit_only_paths"] == [path]
    assert result["reviewed_successors"] == (
        [path] if path in audit.R3R8_REVIEWED_FILES
        or path in audit.R3R8R1_REVIEWED_FILES else []
    )


@pytest.mark.parametrize("path", [
    "phase175_r3r8_pi73_public_connection/unreviewed.py",
    "phase175_r3r8r1_verified_prior_public/unreviewed.py",
    "phase175_r3r7_lemma54_membership/unreviewed.py",
    "src/new_production_rule.py",
])
def test_unknown_addition_still_rejected(repo, path: str) -> None:
    root, start = repo
    file_path = root / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("unreviewed\n", encoding="utf-8")
    end = commit(root, "unknown file")
    with pytest.raises(RuntimeError, match="R3R8R1R1_UNKNOWN_LINEAGE_ADDITION"):
        audit.verify_extended_lineage(
            root, {"preflight": {"head": start}}, {"head": end},
        )


def test_tracked_production_modification_rejected(repo) -> None:
    root, start = repo
    (root / "baseline.py").write_text("production = 2\n", encoding="utf-8")
    end = commit(root, "modify production")
    with pytest.raises(RuntimeError, match="R3R8R1R1_NON_AUDIT_CHANGE_IN_LINEAGE"):
        audit.verify_extended_lineage(
            root, {"preflight": {"head": start}}, {"head": end},
        )


def test_unrelated_head_rejected(repo, tmp_path: Path) -> None:
    root, start = repo
    second = tmp_path / "unrelated"
    second.mkdir()
    git(second, "init", "-q")
    (second / "file.py").write_text("x = 1\n", encoding="utf-8")
    unrelated = commit(second, "different root")
    with pytest.raises(RuntimeError, match="R3R8R1R1_R2_HEAD_NOT_ANCESTOR"):
        audit.verify_extended_lineage(
            root, {"preflight": {"head": unrelated}}, {"head": start},
        )


def test_dirty_or_forged_current_head_rejected(repo) -> None:
    root, start = repo
    with pytest.raises(RuntimeError, match="R3R8R1R1_INVALID_VERIFIED_HEAD"):
        audit.verify_extended_lineage(
            root, {"preflight": {"head": start}}, {"head": "0" * 40},
        )

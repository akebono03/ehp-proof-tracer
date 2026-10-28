"""R10ET-R5C: real Git index checks without changing application sources."""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from phase169_r10et_r5c_preserve_staged_r5.run import (
    REVIEWED_STAGED_R5,
    reviewed_index_snapshot,
)


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args], check=True,
        capture_output=True, text=True, encoding="utf-8",
    ).stdout.strip()


def make_repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "test@example.invalid")
    git(tmp_path, "config", "user.name", "Test")
    (tmp_path / "baseline.txt").write_text("original\n", encoding="utf-8")
    git(tmp_path, "add", "baseline.txt")
    git(tmp_path, "commit", "-qm", "baseline")
    return tmp_path


def test_r5c_real_staged_additions_survive_unstaged_source_edits(tmp_path: Path):
    root = make_repo(tmp_path)
    for path in sorted(REVIEWED_STAGED_R5):
        p = root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("reviewed package addition\n", encoding="utf-8")
    git(root, "add", "phase169_r10et_r5_common_definition_provider")
    expected = reviewed_index_snapshot(root)
    assert expected
    (root / "baseline.txt").write_text("unstaged provider patch\n", encoding="utf-8")
    assert reviewed_index_snapshot(root) == expected
    assert git(root, "diff", "--name-only") == "baseline.txt"


def test_r5c_real_unreviewed_staged_production_change_is_refused(tmp_path: Path):
    root = make_repo(tmp_path)
    (root / "baseline.txt").write_text("unexpected staged edit\n", encoding="utf-8")
    git(root, "add", "baseline.txt")
    with pytest.raises(RuntimeError, match="unreviewed staged"):
        reviewed_index_snapshot(root)

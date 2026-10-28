"""R10ET-R5D: real Git-index test of mixed, immutable staged audit files."""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from phase169_r10et_r5d_staged_audit_guard.run import reviewed_index_snapshot


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


def test_r5d_real_mixed_staged_packages_survive_unstaged_source_edit(tmp_path: Path):
    root = make_repo(tmp_path)
    for folder in (
        "phase169_r10et_r5_common_definition_provider",
        "phase169_r10et_r5b_committed_r4_guard",
    ):
        for item in ("README.md", "tests/test_one.py"):
            path = root / folder / item
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("previously reviewed audit file\n", encoding="utf-8")
        git(root, "add", folder)
    original = reviewed_index_snapshot(root)
    assert original
    (root / "baseline.txt").write_text("unstaged source patch\n", encoding="utf-8")
    assert reviewed_index_snapshot(root) == original
    assert git(root, "diff", "--name-only") == "baseline.txt"
    # The index content and staged path names still have the exact same bytes.
    assert "phase169_r10et_r5_common_definition_provider" in git(
        root, "diff", "--cached", "--name-only",
    )
    assert "phase169_r10et_r5b_committed_r4_guard" in git(
        root, "diff", "--cached", "--name-only",
    )


def test_r5d_real_partial_staged_audit_bundle_is_safe(tmp_path: Path):
    root = make_repo(tmp_path)
    path = root / "phase169_r10et_r5b_committed_r4_guard" / "README.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("audit\n", encoding="utf-8")
    git(root, "add", str(path.relative_to(root)))
    assert reviewed_index_snapshot(root)


@pytest.mark.parametrize("change", ("modified", "production_addition", "unknown_addition"))
def test_r5d_real_unreviewed_index_rejected(tmp_path: Path, change: str):
    root = make_repo(tmp_path)
    if change == "modified":
        (root / "baseline.txt").write_text("staged unexpected edit\n", encoding="utf-8")
        git(root, "add", "baseline.txt")
    else:
        path = root / (
            "phase165_r52_r9_shared_math.py" if change == "production_addition"
            else "unknown_audit/README.md"
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("not reviewed\n", encoding="utf-8")
        git(root, "add", str(path.relative_to(root)))
    with pytest.raises(RuntimeError, match="unreviewed staged"):
        reviewed_index_snapshot(root)

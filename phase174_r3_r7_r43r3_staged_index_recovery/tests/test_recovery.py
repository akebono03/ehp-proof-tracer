"""Tests for R43R3 exact path-filtered index recovery, no real Git mutations."""
from __future__ import annotations

from pathlib import Path
import pytest

from phase174_r3_r7_r43r3_staged_index_recovery.recover import (
    PATHS, validate_index,
)

ROOT = Path(__file__).resolve().parents[1]


def test_exact_twelve_staged_additions_are_eligible():
    entries = tuple(("A", path) for path in PATHS)
    assert len(entries) == 12
    assert validate_index(entries, (), ()) == "EXACT_R43_NEW_FILES_STAGED"


def test_any_extra_staged_or_unstaged_change_is_rejected():
    entries = tuple(("A", path) for path in PATHS)
    with pytest.raises(RuntimeError, match="Unexpected staged"):
        validate_index(entries + (("A", "unrelated.py"),), (), ())
    with pytest.raises(RuntimeError, match="Tracked worktree"):
        validate_index(entries, ("unrelated.py",), ())
    with pytest.raises(RuntimeError, match="Unexpected staged"):
        validate_index(tuple(("M", path) for path in PATHS), (), ())


def test_idempotent_recovery_requires_all_worktree_files_untracked():
    assert validate_index((), (), PATHS) == "ALREADY_UNSTAGED"
    with pytest.raises(RuntimeError, match="not an intact untracked"):
        validate_index((), (), PATHS[:-1])


def test_recovery_never_deletes_worktree_or_changes_production():
    source = (ROOT / "recover.py").read_text(encoding="utf-8")
    script = (ROOT / "run.ps1").read_text(encoding="utf-8")
    assert '"restore", "--staged", "--", *PATHS' in source
    assert '"reset"' not in source
    assert '"clean"' not in source
    assert '"restore", "--worktree"' not in source
    assert 'R43R2 DryRun failed after safe index recovery' in script
    assert 'R43R2/R43R1/R43 validation failed' in script
    assert 'FULL_PYTEST=False' in script

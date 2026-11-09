"""R45 Git blob checks are content-based and do not mutate the worktree."""
from __future__ import annotations

from phase174_r3_r7_r45_ehp_open_obligation_audit.source_guard import (
    PINS,
    git_blob_sha,
    matches_git_blob,
)


def test_pin_table_reviews_core_and_handoff_sources():
    assert "phase165_r52_r9_shared_math.py" in PINS
    assert "phase165_r12_r11_prop42_unified.py" in PINS
    assert "phase174_r3_r7_r44_public_zero_image_tree_frontier/audit.py" in PINS
    assert "phase174_r3_r7_r5_zero_image_hopf_injective/rule.py" in PINS
    assert all(len(sha) == 40 for sha in PINS.values())


def test_blob_matching_accepts_only_exact_or_whole_file_eol_changes():
    raw = b"alpha\nbeta\n"
    sha = git_blob_sha(raw)
    assert matches_git_blob(raw, sha)
    assert matches_git_blob(b"alpha\r\nbeta\r\n", sha)
    assert not matches_git_blob(b"alpha\nBETA\n", sha)
    assert not matches_git_blob(raw, "0" * 40)

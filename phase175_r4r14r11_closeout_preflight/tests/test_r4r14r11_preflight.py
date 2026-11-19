"""Focused R4R14R11 read-only validation; no historical guard tests modified."""
from __future__ import annotations

from phase175_r4r14r11_closeout_preflight.audit import (
    KNOWN_LEGACY_FAILURES, PAIRS, classify_checkout, preflight,
)


def test_k4_preflight_scope_keeps_unfinished_frontiers() -> None:
    assert PAIRS == ((3, 4), (5, 4), (6, 4))
    assert len(KNOWN_LEGACY_FAILURES) == 4
    assert all("phase174_" in name for name in KNOWN_LEGACY_FAILURES)


def test_checkout_classification_does_not_silently_erase_pytest_cache() -> None:
    classified = classify_checkout((".pytest_cache/v/cache/nodeids",))
    assert classified["source_worktree_clean"] is True
    assert classified["tracked_cache_cleanup_needed"] is True
    assert classified["tracked_cache_changes"] == [".pytest_cache/v/cache/nodeids"]


def test_checkout_classification_flags_production_edits() -> None:
    classified = classify_checkout(("phase165_r52_r9_shared_math.py",))
    assert classified["source_worktree_clean"] is False
    assert classified["tracked_non_cache_changes"] == ["phase165_r52_r9_shared_math.py"]


def test_actual_checkout_has_reviewed_source_files() -> None:
    state = preflight()
    assert state["source_worktree_clean"] is True
    assert len(state["source_blobs_at_head"]) == 6
    assert state["historical_guard_status"] == "FOUR_KNOWN_FAILURES_RETAINED_NOT_RERUN"

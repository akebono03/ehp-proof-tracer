"""R49 uses a pinned new GitHub HEAD and reviewed R48 source blobs."""
from __future__ import annotations

from pathlib import Path

from phase174_r3_r7_r49_prop27_upper_delta_tree_frontier.source_guard import (
    REVIEWED_HEAD, PREVIOUS_HEAD, PROP27_BLOBS,
    R48_HANDOFF_BLOBS, ROOT, verify_checkout,
)


def test_guard_contains_reviewed_pins() -> None:
    assert len(REVIEWED_HEAD) == 40
    assert len(PREVIOUS_HEAD) == 40
    assert len(PROP27_BLOBS) == 5
    assert len(R48_HANDOFF_BLOBS) == 4
    assert all(len(sha) == 40 for sha in PROP27_BLOBS.values())
    assert all(len(sha) == 40 for sha in R48_HANDOFF_BLOBS.values())
    assert Path(ROOT).is_absolute()


def test_guard_accepts_reviewed_checkout_only() -> None:
    state = verify_checkout()
    assert state["source_guard"] == "PASS"
    assert state["remote_head"] == REVIEWED_HEAD
    assert state["production_files_changed"] == 0
    assert state["new_givens"] == 0
    assert state["full_pytest"] is False

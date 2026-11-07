"""After applying, assert exact Git path names and unchanged proof semantics."""
from __future__ import annotations

from phase174_r3_r7_r17r1_historical_test_contract.audit import expected_tracked_paths
from phase174_r3_r7_r17r2_windows_git_path_guard_fix.patch import checked_state


def test_live_r17r1_guard_recognizes_git_forward_slashes() -> None:
    assert checked_state() == "EXACT_REVIEWED_PATCH"
    assert expected_tracked_paths(applied=False) == ()
    assert expected_tracked_paths(applied=True) == (
        "phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py",
        "web_group_proof_common.py",
    )

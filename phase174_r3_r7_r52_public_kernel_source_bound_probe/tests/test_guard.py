"""R52 pins actual GitHub R51 merge and reviewed mathematical file content."""
from __future__ import annotations

from phase174_r3_r7_r52_public_kernel_source_bound_probe.source_guard import (
    REVIEWED_HEAD, R51_HANDOFF_BLOBS, R51_PROTECTED_BLOBS, ROOT,
    verify_checkout,
)


def test_new_head_and_r51_handoff_are_reviewed() -> None:
    assert len(REVIEWED_HEAD) == 40
    assert len(R51_HANDOFF_BLOBS) == 3
    assert len(R51_PROTECTED_BLOBS) == 12
    assert ROOT.is_absolute()


def test_source_guard_rejects_modified_production_and_verifies_head() -> None:
    result = verify_checkout()
    assert result["source_guard"] == "PASS"
    assert result["remote_head"] == REVIEWED_HEAD
    assert result["reviewed_files"] == 15
    assert result["production_files_changed"] == 0

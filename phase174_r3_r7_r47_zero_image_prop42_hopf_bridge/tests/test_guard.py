"""R47 must fail closed on unreviewed GitHub checkouts or source edits."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r47_zero_image_prop42_hopf_bridge import source_guard


def test_source_guard_recognizes_current_reviewed_checkout():
    state = source_guard.verify_checkout()
    assert state["source_guard"] == "PASS"
    assert state["remote_head"] == source_guard.REVIEWED_HEAD
    assert state["reviewed_r46_files"] == len(source_guard.REVIEWED_R46_FILES)
    assert state["production_files_changed"] == 0
    assert state["full_pytest"] is False


def test_r47_guard_rejects_modified_reviewed_file(monkeypatch):
    original = source_guard.normalized_sha256
    monkeypatch.setattr(
        source_guard, "normalized_sha256",
        lambda data: "0" * 64,
    )
    with pytest.raises(RuntimeError, match="unreviewed"):
        source_guard.verify_checkout()
    monkeypatch.setattr(source_guard, "normalized_sha256", original)

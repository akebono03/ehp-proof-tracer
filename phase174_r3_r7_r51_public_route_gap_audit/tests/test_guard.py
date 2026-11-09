"""R51 pins the merged R50 review and all public search entry points."""
from __future__ import annotations

from phase174_r3_r7_r51_public_route_gap_audit.source_guard import (
    REVIEWED_BLOBS, REVIEWED_HEAD, git_blob, matches_blob, verify_checkout,
)


def test_source_guard_rejects_unreviewed_blob() -> None:
    assert len(REVIEWED_BLOBS) == 12
    assert len(REVIEWED_HEAD) == 40
    for digest in REVIEWED_BLOBS.values():
        assert len(digest) == 40
    assert matches_blob(b"small", git_blob(b"small"))
    assert not matches_blob(b"changed", git_blob(b"small"))


def test_source_guard_requires_reviewed_live_develop() -> None:
    result = verify_checkout()
    assert result["source_guard"] == "PASS"
    assert result["local_head"] == REVIEWED_HEAD
    assert result["remote_head"] == REVIEWED_HEAD
    assert result["production_files_changed"] == 0
    assert result["full_pytest"] is False

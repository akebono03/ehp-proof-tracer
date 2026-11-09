"""R42 Git hash guard does not make unknown edits look reviewed."""
from __future__ import annotations

from phase174_r3_r7_r42_canonical_search_frontier_audit.source_guard import (
    PINS, PRE_R41_HEAD, REVIEWED_R41_HEAD, git_blob, matches_blob,
)


def test_hashes_and_reviewed_heads_are_pinned():
    assert len(PRE_R41_HEAD) == 40
    assert len(REVIEWED_R41_HEAD) == 40
    assert len(PINS) >= 8
    assert all(len(sha) == 40 for sha in PINS.values())


def test_git_blob_matches_actual_byte_length():
    assert git_blob(b"") == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"
    assert matches_blob(b"alpha\r\nbeta\r\n", git_blob(b"alpha\nbeta\n"))


def test_git_blob_refuses_corrupt_or_short_sha():
    correct = git_blob(b"alpha\nbeta\n")
    assert not matches_blob(b"alpha\nbetx\n", correct)
    assert not matches_blob(b"alpha\nbeta\n", correct[:-1])

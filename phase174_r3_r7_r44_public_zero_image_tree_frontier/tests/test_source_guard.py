"""R44 reviewed source and no-write contract."""
from __future__ import annotations

from phase174_r3_r7_r44_public_zero_image_tree_frontier.source_guard import (
    BASE_HEAD, MERGED_HEAD, BASE_SHA, MERGED_SHA, PINS,
    matches_blob, normalize,
)


def test_reviewed_head_and_sha_pins_are_complete():
    assert len(BASE_HEAD) == len(MERGED_HEAD) == 40
    assert len(BASE_SHA) == len(MERGED_SHA) == 40
    assert all(len(pin) == 40 for pin in PINS.values())
    assert len(PINS) >= 8


def test_source_guard_normalization_accepts_equivalent_line_endings():
    payload = b"one\ntwo\n"
    from phase174_r3_r7_r44_public_zero_image_tree_frontier.source_guard import git_blob
    assert matches_blob(payload, git_blob(payload))
    assert matches_blob(payload.replace(b"\n", b"\r\n"), git_blob(payload))
    assert normalize(payload.replace(b"\n", b"\r\n")) == payload


def test_invalid_blob_pin_rejected_without_disabling_guard():
    assert matches_blob(b"something", "z" * 40) is False
    assert matches_blob(b"something", "123") is False

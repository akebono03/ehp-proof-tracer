"""R46 pinning allows line-ending conversion but not code mutation."""
from __future__ import annotations

from hashlib import sha256

from phase174_r3_r7_r46_prop42_dfs_audit.source_guard import (
    R45_LOCAL_PINS,
    REVIEWED_HEAD,
    REVIEWED_SEARCH_BLOB,
    normalized_sha256,
)


def test_hand_off_pins_cover_r45r1_and_canonical_search():
    assert len(REVIEWED_HEAD) == 40
    assert len(REVIEWED_SEARCH_BLOB) == 40
    assert len(R45_LOCAL_PINS) == 4
    assert "phase174_r3_r7_r45_ehp_open_obligation_audit/run.ps1" in R45_LOCAL_PINS
    assert all(len(value) == 64 for value in R45_LOCAL_PINS.values())


def test_normalized_hash_changes_only_on_non_eol_modifications():
    text = b"a\nb\n"
    expected = sha256(text).hexdigest()
    assert normalized_sha256(text) == expected
    assert normalized_sha256(b"a\r\nb\r\n") == expected
    assert normalized_sha256(b"a\nB\n") != expected

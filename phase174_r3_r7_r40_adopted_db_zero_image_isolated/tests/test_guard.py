"""R40 source pinning and exact-path checks."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r40_adopted_db_zero_image_isolated import source_guard


def test_blob_pin_has_full_forty_hex_digits():
    assert source_guard.PINS
    assert all(len(x) == 40 and set(x) <= set("0123456789abcdef")
               for x in source_guard.PINS.values())
    b = b"alpha\nbeta\n"
    sha = source_guard.git_blob(b)
    assert source_guard.matches_blob(b, sha)
    assert source_guard.matches_blob(b.replace(b"\n", b"\r\n"), sha)
    assert not source_guard.matches_blob(b"tampered", sha)


def test_checkout_protects_real_upstream_sources():
    check = source_guard.verify_checkout()
    assert check["source_guard"] == "PASS"
    assert check["reviewed_source_pins"] == len(source_guard.PINS)


def test_wrong_source_sha_is_rejected(monkeypatch):
    changed = dict(source_guard.PINS)
    changed["sources/toda/Toda_05_2.tex"] = "0" * 40
    monkeypatch.setattr(source_guard, "PINS", changed)
    with pytest.raises(RuntimeError, match="Reviewed source differs"):
        source_guard.verify_checkout()

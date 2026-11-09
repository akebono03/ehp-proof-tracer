"""Exact source fingerprint and checkout fail-closed checks."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r7_r39_verified_zero_image_frontier.source_guard import (
    BASE_HEAD, CONTEXT, PINS, R38_PROVIDER_BLOB,
    git_blob, matches_blob, normalized, verify_checkout,
)


def test_bytewise_git_blob_with_checked_crlf_variants():
    raw = b"line one\nline two\n"
    sha = git_blob(raw)
    assert len(sha) == 40
    assert matches_blob(raw, sha)
    assert matches_blob(raw.replace(b"\n", b"\r\n"), sha)
    assert not matches_blob(b"unexpected", sha)
    assert not matches_blob(raw, sha[:-1])


def test_reviewed_r38_package_and_live_source_are_pinned():
    checkout = verify_checkout()
    assert checkout["source_guard"] == "PASS"
    assert checkout["public_r38_installed"] is True
    assert checkout["local_head"] in (BASE_HEAD, checkout["remote_head"])
    assert len(R38_PROVIDER_BLOB) == 40


def test_wrong_source_pin_is_rejected(monkeypatch):
    import phase174_r3_r7_r39_verified_zero_image_frontier.source_guard as guard
    mutated = dict(guard.PINS)
    mutated["sources/toda/Toda_05_2.tex"] = "0" * 40
    monkeypatch.setattr(guard, "PINS", mutated)
    with pytest.raises(RuntimeError, match="Reviewed source differs"):
        guard.verify_checkout()

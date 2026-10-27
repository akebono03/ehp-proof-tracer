"""Focused safety checks of the R4C2 read-only verifier."""
from __future__ import annotations

import pytest

from phase169_r4c2_committed_audit.verify import (
    R4B_INSERT,
    R4C_INSERT,
    normalized_text,
    verify_provider_source,
)


def fixture_provider(extra: str = "") -> str:
    return (
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n"
        "        options = []\n"
        + R4B_INSERT
        + R4C_INSERT
        + extra
        + "        return options\n"
        + "    return expand\n"
    )


def test_r4c2_accepts_one_adjacent_connection():
    verify_provider_source(fixture_provider())


def test_r4c2_rejects_missing_r4c_connection():
    with pytest.raises(RuntimeError, match="missing or duplicated"):
        verify_provider_source(fixture_provider().replace(R4C_INSERT, ""))


def test_r4c2_rejects_duplicate_r4c_connection():
    with pytest.raises(RuntimeError, match="missing or duplicated"):
        verify_provider_source(fixture_provider(R4C_INSERT))


def test_r4c2_rejects_connection_outside_shared_provider():
    misplaced = (
        "def shared_expansion_provider():\n"
        "    return None\n\n"
        "def unrelated_function():\n"
        "    def expand(goal):\n"
        "        options = []\n"
        + R4B_INSERT
        + R4C_INSERT
        + "        return options\n"
        + "    return expand\n"
    )
    with pytest.raises(RuntimeError, match="not wired inside"):
        verify_provider_source(misplaced)


def test_r4c2_normalizes_only_text_encoding_and_crlf():
    assert normalized_text(b"alpha\r\nbeta\r\n") == "alpha\nbeta\n"
    assert normalized_text(b"\xef\xbb\xbfalpha\n") == "alpha\n"
    assert normalized_text(b"alpha\nbeta\n") != normalized_text(b"alpha\ngamma\n")

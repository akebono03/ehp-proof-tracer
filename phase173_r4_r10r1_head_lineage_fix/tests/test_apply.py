"""Focused tests for the sole R4-R10 HEAD constant correction."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase173_r4_r10r1_head_lineage_fix.apply import (
    NEW_SHA256,
    OLD_SHA256,
    NEW_LINE,
    OLD_LINE,
    REVIEWED_HEAD,
    SOURCE_BLOBS,
    UNCHANGED_CORE_FILES,
    prepared_replacement,
    sha256,
)


def _versions() -> tuple[bytes, bytes]:
    root = Path(__file__).resolve().parents[2]
    replacement = (root / "phase173_r4_r10r1_head_lineage_fix"
                   / "replacement_verify.py.txt").read_bytes()
    original = replacement.replace(NEW_LINE.encode("ascii"), OLD_LINE.encode("ascii"))
    return original, replacement


def test_full_replacement_differs_by_only_one_head_constant() -> None:
    original, replacement = _versions()
    assert sha256(original) == OLD_SHA256
    assert sha256(replacement) == NEW_SHA256
    assert original.count(OLD_LINE.encode("ascii")) == 1
    assert replacement.count(NEW_LINE.encode("ascii")) == 1
    assert prepared_replacement(original, replacement) == replacement


def test_modified_payload_is_refused() -> None:
    original, replacement = _versions()
    with pytest.raises(RuntimeError, match="Original verify.py changed"):
        prepared_replacement(original + b"\n", replacement)
    with pytest.raises(RuntimeError, match="incorrect checksum"):
        prepared_replacement(original, replacement + b"\n")


def test_source_pins_are_not_removed() -> None:
    original, replacement = _versions()
    assert REVIEWED_HEAD.encode("ascii") in replacement
    assert len(SOURCE_BLOBS) == 10
    assert len(UNCHANGED_CORE_FILES) == 3
    assert b'git(root, "status", "--porcelain")' not in replacement
    assert b'git(root, "status", "--porcelain", "--untracked-files=no")' in replacement
    assert original.replace(OLD_LINE.encode("ascii"), NEW_LINE.encode("ascii")) == replacement

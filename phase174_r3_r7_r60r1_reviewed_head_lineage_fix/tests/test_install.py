"""R60R1 exact lineage patch tests; no production or mathematical changes."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r7_r60r1_reviewed_head_lineage_fix.install import (
    AFTER_SHA256,
    BEFORE_SHA256,
    EXPECTED_BLOB_PINS,
    NEW_LINE,
    OLD_LINE,
    REVIEWED_HEAD,
    TARGET,
    checked_patch,
    git_head,
    preflight,
    sha256_bytes,
)


def test_r60r1_reviewed_head_is_current_develop() -> None:
    root = Path(__file__).resolve().parents[2]
    assert REVIEWED_HEAD == "17b96a63c1ee400d587c14c785c4c1e697334206"
    assert git_head(root) == REVIEWED_HEAD
    assert len(EXPECTED_BLOB_PINS) == 6


def test_r60r1_exact_patch_changes_only_one_line() -> None:
    root = Path(__file__).resolve().parents[2]
    original_full = (root / "phase174_r3_r7_r60_reference_ownership_audit"
                     / "audit.py").read_bytes()
    updated, required = checked_patch(original_full)
    assert not required
    assert updated == original_full
    assert sha256_bytes(updated.replace(b"\r\n", b"\n")) == AFTER_SHA256
    assert updated.count(NEW_LINE.encode("ascii")) == 1
    reverted = updated.replace(NEW_LINE.encode("ascii"), OLD_LINE.encode("ascii"))
    assert sha256_bytes(reverted.replace(b"\r\n", b"\n")) == BEFORE_SHA256
    reconstructed, should_change = checked_patch(reverted)
    assert should_change
    assert reconstructed == updated


@pytest.mark.parametrize("bad", (b"", b"REVIEWED_HEAD = 'wrong'\n", b"different source\n"))
def test_r60r1_rejects_unreviewed_audit_file(bad: bytes) -> None:
    with pytest.raises(RuntimeError, match="PIN_MISMATCH"):
        checked_patch(bad)


def test_r60r1_preflight_preserves_six_source_pins() -> None:
    root = Path(__file__).resolve().parents[2]
    path, updated, required = preflight(root)
    assert path == root / TARGET
    assert not required
    assert sha256_bytes(updated.replace(b"\r\n", b"\n")) == AFTER_SHA256

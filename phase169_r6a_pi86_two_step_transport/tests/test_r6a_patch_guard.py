"""Patch identity and full-function export are verified without repository imports."""
from __future__ import annotations

import pytest

from phase169_r6a_pi86_two_step_transport.patch import (
    OLD, NEW, full_function, patched_content,
)


def _stub() -> bytes:
    return (
        "def shared_expansion_provider():\n"
        "    def expand(goal, available, bridge, proof_target):\n"
        + OLD
        + "        return options\n"
        + "    return expand\n"
    ).encode("utf-8")


def test_r6a_patch_changes_only_the_unique_reviewed_anchor():
    original = _stub()
    updated = patched_content(original, original)
    assert updated.count(NEW.encode()) == 1
    assert original.decode() in updated.decode().replace(NEW, OLD)
    assert "expand_prior_two_step_eta_square_transport" in full_function(updated)


def test_r6a_patch_rejects_dirty_baseline_and_duplicate_anchor():
    original = _stub()
    with pytest.raises(RuntimeError, match="differs"):
        patched_content(original + b"\n", original)
    with pytest.raises(RuntimeError, match="duplicated"):
        patched_content(original.replace(OLD.encode(), (OLD + OLD).encode()),
                        original.replace(OLD.encode(), (OLD + OLD).encode()))


def test_r6a_patch_preserves_windows_newlines_and_rejects_repeat():
    before = _stub().replace(b"\n", b"\r\n")
    updated = patched_content(before, before)
    assert b"\r\n" in updated
    with pytest.raises(RuntimeError):
        patched_content(updated, updated)

"""Guarded patch tests for R20R8 (no root files changed)."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase171_r20r8_public_double_nonzero.install import (
    PROVIDER_FLAG,
    SOURCE_FLAG,
    R20R7_ORDER_ANCHOR,
    adapt,
    checked_worktree,
    expected_r20r7,
    normalize,
    patched_text,
)
import phase171_r20r8_public_double_nonzero.install as installer


def _reviewed_mock():
    source = "def expand_public_order_four_from_nonzero_double(goal):\n    return ()\n"
    provider = "def shared_expansion_provider():\n" + R20R7_ORDER_ANCHOR
    return expected_r20r7(source, provider)


def test_appends_only_r20r8_and_is_idempotent() -> None:
    s, p = _reviewed_mock()
    next_s, next_p = patched_text(s, p)
    assert next_s.count(SOURCE_FLAG) == 1
    assert next_p.count(PROVIDER_FLAG) == 1
    assert patched_text(next_s, next_p) == (next_s, next_p)


def test_rejects_partial_or_missing_baseline() -> None:
    s, p = _reviewed_mock()
    ns, np = patched_text(s, p)
    with pytest.raises(RuntimeError, match="partial"):
        patched_text(ns, p)
    with pytest.raises(RuntimeError, match="partial"):
        patched_text(s, np)
    with pytest.raises(RuntimeError, match="anchor"):
        patched_text(s, "def shared_expansion_provider():\n")


def test_preserves_crlf() -> None:
    s, p = _reviewed_mock()
    ns, np = patched_text(s, p)
    assert normalize(adapt(ns, s.replace("\n", "\r\n").encode("utf-8"))) == ns
    assert b"\r\n" in adapt(np, p.replace("\n", "\r\n").encode("utf-8"))


def test_source_guard_accepts_committed_or_uncommitted_r20r7(monkeypatch, tmp_path: Path) -> None:
    before = _reviewed_mock()
    originals = {
        installer.SOURCE: "def expand_public_order_four_from_nonzero_double(goal):\n    return ()\n",
        installer.PROVIDER: "def shared_expansion_provider():\n" + R20R7_ORDER_ANCHOR,
    }
    for path, content in zip((installer.SOURCE, installer.PROVIDER), before):
        dest = tmp_path / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(content.replace("\n", "\r\n").encode("utf-8"))
    def fake_git(*args):
        if args == ("branch", "--show-current"):
            return b"develop"
        if args == ("rev-parse", "HEAD"):
            return b"head-after-r20r7"
        if len(args) == 2 and args[0] == "rev-parse" and ":" in args[1]:
            path = Path(args[1].split(":", 1)[1])
            return installer.REVIEWED_BLOBS[path].encode("ascii")
        if len(args) == 2 and args[0] == "show":
            path = Path(args[1].split(":", 1)[1])
            return originals[path].encode("utf-8")
        raise AssertionError(args)
    monkeypatch.setattr(installer, "ROOT", tmp_path)
    monkeypatch.setattr(installer, "git", fake_git)
    head, _, recorded_before, recorded_after = checked_worktree()
    assert head == "head-after-r20r7"
    assert tuple(recorded_before.values()) == before
    assert all(SOURCE_FLAG in recorded_after[installer.SOURCE] for _ in (1,))
    # This is a content guard: it is deliberately independent of Git HEAD's
    # blob for R20R7, permitting subsequent commits without weakening drift.
    target = tmp_path / installer.SOURCE
    target.write_bytes(target.read_bytes() + b"\r\n# unreviewed change\r\n")
    with pytest.raises(RuntimeError, match="unexpected local edit"):
        checked_worktree()

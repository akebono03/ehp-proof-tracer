"""Strict predecessor checks for the R4C1 patcher (offline, no production edits)."""
from __future__ import annotations

import pytest

from phase169_r4c_pi64_suspension_iso import patch


def _git_hash(data: bytes) -> str:
    return patch.git_blob_hash(data)


def _base() -> bytes:
    return (
        "def shared_expansion_provider(bridge):\n"
        + patch.R4B_ANCHOR
        + "        return options\n"
    ).encode("utf-8")


def test_r4c1_accepts_pre_r4b_head_with_only_local_r4b(monkeypatch):
    original = _base()
    monkeypatch.setattr(patch, "EXPECTED_PRE_R4B_GIT_BLOB", _git_hash(original))
    worktree = patch.expected_r4b_source(original.decode("utf-8")).encode("utf-8")
    normalized, kind = patch.verified_r4b_worktree(_git_hash(original), original, worktree)
    assert normalized.encode("utf-8") == worktree
    assert kind == "R4B_UNCOMMITTED"


def test_r4c1_accepts_committed_r4b_with_crlf(monkeypatch):
    original = _base().replace(b"\n", b"\r\n")
    r4b = patch.expected_r4b_source(original.decode("utf-8").replace("\r\n", "\n"))
    committed = r4b.replace("\n", "\r\n").encode("utf-8")
    monkeypatch.setattr(patch, "EXPECTED_PRE_R4B_GIT_BLOB", _git_hash(original))
    monkeypatch.setattr(patch, "EXPECTED_COMMITTED_R4B_GIT_BLOB", _git_hash(committed))
    normalized, kind = patch.verified_r4b_worktree(_git_hash(committed), committed, committed)
    assert normalized == r4b
    assert kind == "R4B_COMMITTED"


def test_r4c1_rejects_unrelated_local_change_even_on_committed_r4b(monkeypatch):
    original = _base()
    committed = patch.expected_r4b_source(original.decode("utf-8")).encode("utf-8")
    monkeypatch.setattr(patch, "EXPECTED_PRE_R4B_GIT_BLOB", _git_hash(original))
    monkeypatch.setattr(patch, "EXPECTED_COMMITTED_R4B_GIT_BLOB", _git_hash(committed))
    with pytest.raises(RuntimeError, match="not exactly the audited R4B state"):
        patch.verified_r4b_worktree(_git_hash(committed), committed, committed + b"# unrelated\n")


def test_r4c1_rejects_unaudited_git_head():
    original = _base()
    with pytest.raises(RuntimeError, match="unrecognized Git HEAD"):
        patch.verified_r4b_worktree(_git_hash(original), original, original)


def test_r4c1_rejects_claimed_blob_with_inconsistent_bytes():
    with pytest.raises(RuntimeError, match="blob and retrieved bytes"):
        patch.verified_r4b_worktree(patch.EXPECTED_COMMITTED_R4B_GIT_BLOB, _base(), _base())


def test_r4c1_rejects_r4c_already_applied(monkeypatch):
    original = _base()
    committed = patch.expected_r4b_source(original.decode("utf-8")).encode("utf-8")
    monkeypatch.setattr(patch, "EXPECTED_PRE_R4B_GIT_BLOB", _git_hash(original))
    monkeypatch.setattr(patch, "EXPECTED_COMMITTED_R4B_GIT_BLOB", _git_hash(committed))
    already = committed.replace(patch.R4B_INSERT.encode("utf-8"),
                                (patch.R4B_INSERT + patch.R4C_INSERT).encode("utf-8"))
    with pytest.raises(RuntimeError, match="not exactly the audited R4B state"):
        patch.verified_r4b_worktree(_git_hash(committed), committed, already)

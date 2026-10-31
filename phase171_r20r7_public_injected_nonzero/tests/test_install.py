"""Deterministic patch and CRLF regression tests, without changing root sources."""
from __future__ import annotations

from pathlib import Path

import pytest

import phase171_r20r7_public_injected_nonzero.install as installer
from phase171_r20r7_public_injected_nonzero.install import (
    PROVIDER_FLAG,
    R20R6_ANCHOR,
    R20R7_ANCHOR,
    SOURCE_FLAG,
    adapt,
    expected_r20r6,
    normalize,
    patched_text,
)


def _reviewed_mock():
    source = "from __future__ import annotations\n\ndef inferred_order_four_rule(goal):\n    return goal\n"
    provider = (
        "def shared_expansion_provider():\n"
        + R20R6_ANCHOR
        + "    return ()\n"
    )
    return expected_r20r6(source, provider)


def test_install_follows_exact_reviewed_r20r6_patch() -> None:
    earlier_source, earlier_provider = _reviewed_mock()
    new_source, new_provider = patched_text(earlier_source, earlier_provider)
    assert new_source.count(SOURCE_FLAG) == 1
    assert new_provider.count(PROVIDER_FLAG) == 1
    assert new_provider.count(R20R7_ANCHOR) == 1
    assert patched_text(new_source, new_provider) == (new_source, new_provider)


def test_install_rejects_half_patch_and_drift() -> None:
    earlier_source, earlier_provider = _reviewed_mock()
    new_source, new_provider = patched_text(earlier_source, earlier_provider)
    with pytest.raises(RuntimeError, match="partial"):
        patched_text(new_source, earlier_provider)
    with pytest.raises(RuntimeError, match="partial"):
        patched_text(earlier_source, new_provider)
    with pytest.raises(RuntimeError, match="provider call"):
        patched_text(earlier_source, "def shared_expansion_provider():\n    return ()\n")


def test_install_keeps_original_crlf_or_lf() -> None:
    earlier_source, earlier_provider = _reviewed_mock()
    new_source, new_provider = patched_text(earlier_source, earlier_provider)
    crlf = adapt(new_source, earlier_source.replace("\n", "\r\n").encode("utf-8"))
    assert b"\r\n" in crlf
    assert normalize(crlf) == new_source
    assert adapt(new_provider, earlier_provider.encode("utf-8")).decode("utf-8") == new_provider


def _check_mock_worktree(monkeypatch, tmp_path: Path, *, committed: bool, mixed: bool = False):
    """Simulate reviewed Git contents without touching the actual repository."""
    r20r6_source, r20r6_provider = _reviewed_mock()
    legacy_source = "from __future__ import annotations\n\ndef inferred_order_four_rule(goal):\n    return goal\n"
    legacy_provider = "def shared_expansion_provider():\n" + R20R6_ANCHOR + "    return ()\n"
    # Pre-commit HEAD contains the older sources; its worktree already has R20R6.
    files = {
        installer.SOURCE: r20r6_source if committed else legacy_source,
        installer.PROVIDER: r20r6_provider if committed else legacy_provider,
    }
    worktree = {installer.SOURCE: r20r6_source, installer.PROVIDER: r20r6_provider}
    early_ids = {installer.SOURCE: "early-source", installer.PROVIDER: "early-provider"}
    committed_ids = {installer.SOURCE: "r20r6-source", installer.PROVIDER: "r20r6-provider"}
    ids = dict(committed_ids if committed else early_ids)
    if mixed:
        ids[installer.PROVIDER] = early_ids[installer.PROVIDER] if committed else committed_ids[installer.PROVIDER]
    for path, content in files.items():
        dest = tmp_path / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        # Exact bytes that a clean worktree would contain, CRLF included.
        dest.write_bytes(worktree[path].replace("\n", "\r\n").encode("utf-8"))
    def fake_git_read(*arguments: str) -> bytes:
        if arguments == ("branch", "--show-current"):
            return b"develop"
        if arguments == ("rev-parse", "HEAD"):
            return b"test-head"
        if len(arguments) == 2 and arguments[1].startswith("HEAD:"):
            path = Path(arguments[1][5:])
            if arguments[0] == "rev-parse":
                return ids[path].encode("ascii")
            if arguments[0] == "show":
                return files[path].encode("utf-8")
        raise AssertionError("unexpected Git command: " + repr(arguments))
    monkeypatch.setattr(installer, "ROOT", tmp_path)
    monkeypatch.setattr(installer, "git_read", fake_git_read)
    monkeypatch.setattr(installer, "REVIEWED_HEAD_BLOBS", early_ids)
    monkeypatch.setattr(installer, "REVIEWED_R20R6_COMMITTED_BLOBS", committed_ids)
    return r20r6_source, r20r6_provider


def test_checked_worktree_accepts_committed_r20r6_pair(monkeypatch, tmp_path: Path) -> None:
    original_source, original_provider = _check_mock_worktree(
        monkeypatch, tmp_path, committed=True,
    )
    head, originals, before, after = installer.checked_worktree()
    assert head == "test-head"
    assert before == {
        installer.SOURCE: original_source,
        installer.PROVIDER: original_provider,
    }
    assert all(b"\r\n" in originals[path] for path in (installer.SOURCE, installer.PROVIDER))
    assert after[installer.SOURCE].count(SOURCE_FLAG) == 1
    assert after[installer.PROVIDER].count(PROVIDER_FLAG) == 1


def test_checked_worktree_accepts_precommit_r20r6_pair(monkeypatch, tmp_path: Path) -> None:
    original_source, original_provider = _check_mock_worktree(
        monkeypatch, tmp_path, committed=False,
    )
    _, _, before, after = installer.checked_worktree()
    assert before[installer.SOURCE] == original_source
    assert before[installer.PROVIDER] == original_provider
    assert after[installer.SOURCE].count(SOURCE_FLAG) == 1
    assert after[installer.PROVIDER].count(PROVIDER_FLAG) == 1


def test_checked_worktree_rejects_mixed_git_baselines(monkeypatch, tmp_path: Path) -> None:
    _check_mock_worktree(monkeypatch, tmp_path, committed=True, mixed=True)
    with pytest.raises(RuntimeError, match="mixed R20R6"):
        installer.checked_worktree()


def test_checked_worktree_rejects_unreviewed_local_edits(monkeypatch, tmp_path: Path) -> None:
    _check_mock_worktree(monkeypatch, tmp_path, committed=True)
    target = tmp_path / installer.SOURCE
    target.write_bytes(target.read_bytes() + b"\r\n# extra edit\r\n")
    with pytest.raises(RuntimeError, match="unexpected local edits"):
        installer.checked_worktree()

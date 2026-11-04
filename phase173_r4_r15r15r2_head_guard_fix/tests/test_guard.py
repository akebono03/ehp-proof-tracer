"""The guard permits reviewed descendants, never unreviewed source content."""
from __future__ import annotations

from pathlib import Path
from subprocess import CompletedProcess

import pytest

from phase173_r4_r15r15r2_head_guard_fix import install


def _mock_source_tree(monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
                      *, changed: str | None = None, bad_blob: str | None = None) -> str:
    """Set up only the filesystem and git results consumed by Source Guard."""
    for path in install.REVIEWED_BLOBS:
        destination = tmp_path / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("reviewed source\n", encoding="utf-8")
    monkeypatch.setattr(install, "ROOT", tmp_path)
    head = "a" * 40

    def fake_git(*args: str) -> str:
        if args == ("branch", "--show-current"):
            return "develop"
        if args in (("rev-parse", "HEAD"), ("rev-parse", "origin/develop")):
            return head
        if args == ("diff", "--cached", "--name-only"):
            return ""
        if args == ("diff", "--name-only"):
            return changed or ""
        if len(args) == 2 and args[0] == "rev-parse" and args[1].startswith("HEAD:"):
            path = args[1][5:]
            if path not in install.REVIEWED_BLOBS:
                raise AssertionError("unexpected git path")
            if path == bad_blob:
                return "b" * 40
            return install.REVIEWED_BLOBS[path]
        raise AssertionError("unexpected git command: " + repr(args))

    def fake_command(*args: str) -> CompletedProcess[str]:
        assert args == ("merge-base", "--is-ancestor", install.REVIEWED_HEAD, "HEAD")
        return CompletedProcess(args=args, returncode=0, stdout="", stderr="")

    monkeypatch.setattr(install, "git", fake_git)
    monkeypatch.setattr(install, "command", fake_command)
    return head


def test_reviewed_descendant_is_accepted(monkeypatch: pytest.MonkeyPatch,
                                        tmp_path: Path) -> None:
    expected = _mock_source_tree(monkeypatch, tmp_path)
    assert install.source_guard(installed=False) == expected


def test_reviewed_blob_mismatch_is_rejected(monkeypatch: pytest.MonkeyPatch,
                                           tmp_path: Path) -> None:
    _mock_source_tree(monkeypatch, tmp_path, bad_blob="web_group_proof_common.py")
    with pytest.raises(RuntimeError, match="reviewed content changed"):
        install.source_guard(installed=False)


def test_unreviewed_local_tracked_edits_are_rejected(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    _mock_source_tree(monkeypatch, tmp_path, changed="templates/index.html")
    with pytest.raises(RuntimeError, match="unreviewed tracked local changes"):
        install.source_guard(installed=False)

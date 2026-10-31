"""A changing commit is allowed only for content-identical source states."""
from __future__ import annotations

from pathlib import Path

import pytest

import phase171_r20r13r2_multiple_blank_eta_merge.install as installer


def _test_worktree(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, *,
                   recorded: bytes | None = None, current: bytes | None = None,
                   with_hook: bool = True) -> bytes:
    original = (installer.HERE / "reviewed_projection.py").read_bytes()
    target = tmp_path / installer.TARGET
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(original if current is None else current)
    renderer = tmp_path / installer.RENDERER
    renderer.parent.mkdir(parents=True, exist_ok=True)
    renderer.write_text(
        "format_complete_proof_sentences(lines, model)" if with_hook else "unrelated code",
        encoding="utf-8",
    )
    monkeypatch.setattr(installer, "ROOT", tmp_path)
    monkeypatch.setattr(installer, "git", lambda *args:
                        "develop" if args == ("branch", "--show-current") else "a-new-develop-HEAD")
    monkeypatch.setattr(installer, "committed_projection",
                        lambda: original if recorded is None else recorded)
    return original


def test_new_commit_with_exact_reviewed_content_is_accepted(monkeypatch, tmp_path):
    original = _test_worktree(monkeypatch, tmp_path)
    head, before, after, already = installer.preflight()
    assert head == "a-new-develop-HEAD"
    assert before == original
    assert already is False
    assert installer.sha256(installer.normalized(after)) == installer.CORRECTED_SHA256


def test_new_commit_with_unreviewed_tracked_content_is_rejected(monkeypatch, tmp_path):
    _test_worktree(monkeypatch, tmp_path, recorded=b"not the reviewed source")
    before = (tmp_path / installer.TARGET).read_bytes()
    with pytest.raises(RuntimeError, match="HEAD projection content is not reviewed"):
        installer.preflight()
    assert (tmp_path / installer.TARGET).read_bytes() == before


def test_unreviewed_worktree_is_rejected_even_when_head_matches(monkeypatch, tmp_path):
    _test_worktree(monkeypatch, tmp_path, current=b"malformed local projection")
    with pytest.raises(RuntimeError, match="target projection differs"):
        installer.preflight()


def test_already_corrected_content_is_idempotent(monkeypatch, tmp_path):
    corrected = (installer.HERE / "corrected_projection.py").read_bytes()
    _test_worktree(monkeypatch, tmp_path, recorded=corrected, current=corrected)
    head, before, after, already = installer.preflight()
    assert head == "a-new-develop-HEAD"
    assert before == after == corrected
    assert already is True


def test_renderer_hook_is_still_required(monkeypatch, tmp_path):
    _test_worktree(monkeypatch, tmp_path, with_hook=False)
    with pytest.raises(RuntimeError, match="renderer hook missing"):
        installer.preflight()

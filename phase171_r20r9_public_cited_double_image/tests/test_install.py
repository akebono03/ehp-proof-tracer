"""Installer guards, content reconstruction, line endings and idempotence."""
from __future__ import annotations

from pathlib import Path

import pytest

import phase171_r20r9_public_cited_double_image.install as installer


def _fixture():
    reviewed = {
        installer.R7_SOURCE: (
            "def expand_public_injected_generator_nonzero(goal):\n    return ()\n"
        ),
        installer.DOUBLE_SOURCE: "def typed_double_image_rule(goal):\n    return ()\n",
        installer.PROVIDER: "def shared_expansion_provider():\n" + installer.R8_ANCHOR,
    }
    return reviewed


def test_expected_content_only_adds_r20r8_then_r20r9() -> None:
    before = installer.expected_r20r8(_fixture())
    after = installer.patched_text(before)
    assert before[installer.R7_SOURCE] != _fixture()[installer.R7_SOURCE]
    assert after[installer.R7_SOURCE] == before[installer.R7_SOURCE]
    assert after[installer.DOUBLE_SOURCE].count(installer.R9_SOURCE_FLAG) == 1
    assert after[installer.PROVIDER].count(installer.R9_PROVIDER_FLAG) == 1
    assert installer.R9_PROVIDER_FLAG not in before[installer.PROVIDER]


def test_duplicate_or_missing_provider_anchor_rejected() -> None:
    before = installer.expected_r20r8(_fixture())
    changed = dict(before)
    changed[installer.PROVIDER] = "def shared_expansion_provider():\n"
    with pytest.raises(RuntimeError, match="anchor"):
        installer.patched_text(changed)
    changed[installer.PROVIDER] = before[installer.PROVIDER] + installer.R8_LINE
    with pytest.raises(RuntimeError, match="anchor"):
        installer.patched_text(changed)


def test_crlf_preserved() -> None:
    before = installer.expected_r20r8(_fixture())
    after = installer.patched_text(before)
    data = installer.adapt(after[installer.PROVIDER], before[installer.PROVIDER].replace("\n", "\r\n").encode("utf-8"))
    assert b"\r\n" in data
    assert installer.normalize(data) == after[installer.PROVIDER]


def test_checked_worktree_accepts_commit_transition_and_rejects_partial(monkeypatch, tmp_path: Path) -> None:
    reviewed = _fixture()
    before = installer.expected_r20r8(reviewed)
    after = installer.patched_text(before)
    for path in reviewed:
        dest = tmp_path / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(installer.adapt(before[path], b"\r\n"))

    def fake_git(*args):
        if args == ("branch", "--show-current"):
            return b"develop"
        if args == ("rev-parse", "HEAD"):
            return b"new-committed-head"
        if args[0] == "rev-parse":
            return installer.REVIEWED_BLOBS[Path(args[1].split(":", 1)[1])].encode("ascii")
        if args[0] == "show":
            return reviewed[Path(args[1].split(":", 1)[1])].encode("utf-8")
        raise AssertionError(args)

    monkeypatch.setattr(installer, "ROOT", tmp_path)
    monkeypatch.setattr(installer, "git", fake_git)
    head, _, old, new = installer.checked_worktree()
    assert head == "new-committed-head"
    assert old == before and new == after
    # Upgrade exactly the R20R9R1 version that is present in the user worktree.
    legacy = installer.legacy_r20r9_text(before)
    assert legacy[installer.DOUBLE_SOURCE] != after[installer.DOUBLE_SOURCE]
    assert legacy[installer.PROVIDER] == after[installer.PROVIDER]
    for path in (installer.DOUBLE_SOURCE, installer.PROVIDER):
        (tmp_path / path).write_bytes(installer.adapt(legacy[path], b"\r\n"))
    installer.checked_worktree()
    previous = installer.r20r9r2_text(before)
    assert previous[installer.DOUBLE_SOURCE] != after[installer.DOUBLE_SOURCE]
    assert previous[installer.PROVIDER] == after[installer.PROVIDER]
    for path in (installer.DOUBLE_SOURCE, installer.PROVIDER):
        (tmp_path / path).write_bytes(installer.adapt(previous[path], b"\r\n"))
    installer.checked_worktree()
    for path in (installer.DOUBLE_SOURCE, installer.PROVIDER):
        (tmp_path / path).write_bytes(installer.adapt(after[path], b"\r\n"))
    installer.checked_worktree()
    (tmp_path / installer.PROVIDER).write_text(before[installer.PROVIDER], encoding="utf-8")
    with pytest.raises(RuntimeError, match="partial"):
        installer.checked_worktree()


def test_correct_dimension_guard_and_exact_legacy_upgrade() -> None:
    before = installer.expected_r20r8(_fixture())
    corrected = installer.patched_text(before)
    previous = installer.r20r9r2_text(before)
    legacy = installer.legacy_r20r9_text(before)
    assert corrected[installer.DOUBLE_SOURCE].count(installer.CORRECT_SOURCE_DIMENSION_GUARD) == 1
    assert corrected[installer.DOUBLE_SOURCE].count(installer.LEGACY_SOURCE_DIMENSION_GUARD) == 0
    assert corrected[installer.DOUBLE_SOURCE].count(installer.R20R9R4_CITED_TARGET_GUARD) == 1
    assert corrected[installer.DOUBLE_SOURCE].count(installer.R20R9R2_CITED_TARGET_GUARD) == 0
    assert corrected[installer.DOUBLE_SOURCE].count(installer.R20R9R4_GENERATOR_IMAGE_BLOCK) == 1
    assert corrected[installer.DOUBLE_SOURCE].count(installer.R20R9R2_GENERATOR_IMAGE_BLOCK) == 0
    assert previous[installer.DOUBLE_SOURCE].count(installer.CORRECT_SOURCE_DIMENSION_GUARD) == 1
    assert previous[installer.DOUBLE_SOURCE].count(installer.R20R9R2_CITED_TARGET_GUARD) == 1
    assert previous[installer.DOUBLE_SOURCE].count(installer.R20R9R4_CITED_TARGET_GUARD) == 0
    assert previous[installer.DOUBLE_SOURCE].count(installer.R20R9R2_GENERATOR_IMAGE_BLOCK) == 1
    assert previous[installer.DOUBLE_SOURCE].count(installer.R20R9R4_GENERATOR_IMAGE_BLOCK) == 0
    assert legacy[installer.DOUBLE_SOURCE].count(installer.LEGACY_SOURCE_DIMENSION_GUARD) == 1
    assert legacy[installer.DOUBLE_SOURCE].count(installer.R20R9R2_CITED_TARGET_GUARD) == 1
    assert legacy[installer.DOUBLE_SOURCE].count(installer.CORRECT_SOURCE_DIMENSION_GUARD) == 0
    assert legacy[installer.PROVIDER] == corrected[installer.PROVIDER]
    assert previous[installer.PROVIDER] == corrected[installer.PROVIDER]

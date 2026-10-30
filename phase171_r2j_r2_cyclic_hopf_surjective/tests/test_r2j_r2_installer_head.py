"""R2J-R2 R1: only audited Git commits and the unchanged shared module are accepted."""
from __future__ import annotations

import pytest

from phase171_r2j_r2_cyclic_hopf_surjective import install


BASELINE = (
    "def shared_expansion_provider():\n"
    "    def expand(goal):\n"
    "        options = []\n"
    + install.ANCHOR
    + "        return tuple(options)\n"
    "    return expand\n"
)


def _environment(monkeypatch, tmp_path, *, head, blob=None, diff="", installed=False):
    original = BASELINE.encode("utf-8")
    if installed:
        original = install._render_source_with_hook(original)
    target = tmp_path / "phase165_r52_r9_shared_math.py"
    target.write_bytes(original)
    monkeypatch.setattr(install, "ROOT", tmp_path)
    monkeypatch.setattr(install, "TARGET", target)

    def fake_git(*args):
        if args == ("branch", "--show-current"):
            return "develop"
        if args == ("rev-parse", "HEAD"):
            return head
        if args == ("rev-parse", "HEAD:phase165_r52_r9_shared_math.py"):
            return install.EXPECTED_SHARED_BLOB if blob is None else blob
        if args == ("diff", "--", "phase165_r52_r9_shared_math.py"):
            return diff
        raise AssertionError("unhandled git invocation: " + repr(args))

    monkeypatch.setattr(install, "_git", fake_git)
    return original


@pytest.mark.parametrize("head", install.EXPECTED_BASE_HEADS)
def test_audited_head_with_unchanged_shared_module_passes(monkeypatch, tmp_path, head):
    original = _environment(monkeypatch, tmp_path, head=head)
    raw, installed = install.preflight()
    assert raw == original
    assert installed is False


def test_changed_git_blob_rejected(monkeypatch, tmp_path):
    _environment(
        monkeypatch, tmp_path, head=install.EXPECTED_BASE_HEADS[-1], blob="0" * 40,
    )
    with pytest.raises(RuntimeError, match="blob differs"):
        install.preflight()


def test_unreviewed_head_rejected(monkeypatch, tmp_path):
    _environment(monkeypatch, tmp_path, head="0" * 40)
    with pytest.raises(RuntimeError, match="unexpected HEAD"):
        install.preflight()


def test_tracked_shared_edit_rejected(monkeypatch, tmp_path):
    _environment(
        monkeypatch, tmp_path, head=install.EXPECTED_BASE_HEADS[-1],
        diff="diff --git a/phase165_r52_r9_shared_math.py b/phase165_r52_r9_shared_math.py",
    )
    with pytest.raises(RuntimeError, match="existing tracked edit"):
        install.preflight()


def test_existing_hook_can_be_checked_idempotently(monkeypatch, tmp_path):
    original = _environment(
        monkeypatch, tmp_path, head="0" * 40, installed=True,
    )
    raw, installed = install.preflight()
    assert raw == original
    assert installed is True

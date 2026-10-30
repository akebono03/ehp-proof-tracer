"""R2J-R3 installer regressions for a committed R2J-R2 baseline.

These tests are deliberately self-contained and require neither a GitHub
connection nor the earlier transient R2J-R2 install.py module.
"""
from __future__ import annotations

import subprocess
from types import SimpleNamespace

import pytest

from phase171_r2j_r3_ehp_exactness import install


def _baseline() -> bytes:
    return (
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n"
        + install.ANCHOR
        + "        return ()\n"
        + "    return expand\n"
    ).encode("utf-8")


def _fixture(monkeypatch, tmp_path, *, eol="\n"):
    baseline = _baseline()
    target = tmp_path / "phase165_r52_r9_shared_math.py"
    content = baseline.replace(b"\n", eol.encode("ascii"))
    target.write_bytes(content)
    output = tmp_path / "output"
    monkeypatch.setattr(install, "ROOT", tmp_path)
    monkeypatch.setattr(install, "TARGET", target)
    monkeypatch.setattr(install, "BACKUP", output / "before.py")
    monkeypatch.setattr(install, "STATE", output / "state.json")
    monkeypatch.setattr(install, "R2J_R2_SHARED_BLOB", install._git_blob_sha(baseline))
    monkeypatch.setattr(install, "_git_bytes", lambda *args: baseline)
    monkeypatch.setattr(install, "_git", lambda *args: (
        "develop" if args == ("branch", "--show-current") else
        "future-head" if args == ("rev-parse", "HEAD") else
        install.R2J_R2_SHARED_BLOB if args == (
            "rev-parse", "HEAD:phase165_r52_r9_shared_math.py"
        ) else ""
    ))
    monkeypatch.setattr(
        install.subprocess, "run",
        lambda *args, **kwargs: SimpleNamespace(returncode=0),
    )
    return target, baseline


def test_committed_r2j_r2_is_available_without_transient_installer(monkeypatch, tmp_path):
    target, baseline = _fixture(monkeypatch, tmp_path)
    assert install._exact_r2j_r2_baseline() == baseline
    observed, installed = install.preflight()
    assert observed == target.read_bytes()
    assert installed is False


def test_committed_r2j_r2_allows_crlf_checkout_without_rewriting_others(monkeypatch, tmp_path):
    target, baseline = _fixture(monkeypatch, tmp_path, eol="\r\n")
    observed, installed = install.preflight()
    assert installed is False
    modified = install._insert_hook(observed)
    assert b"\r\n" in modified
    assert modified.replace(b"\r\n", b"\n") == install._insert_hook(baseline)
    assert target.read_bytes() == observed


def test_committed_r2j_r2_rejects_unreviewed_worktree_change(monkeypatch, tmp_path):
    target, _ = _fixture(monkeypatch, tmp_path)
    target.write_bytes(target.read_bytes().replace(b"return ()", b"return (goal,)"))
    with pytest.raises(RuntimeError, match="unexpected shared-module bytes"):
        install.preflight()


def test_committed_r2j_r2_rejects_wrong_head_blob(monkeypatch, tmp_path):
    _fixture(monkeypatch, tmp_path)
    monkeypatch.setattr(install, "_git", lambda *args: (
        "develop" if args == ("branch", "--show-current") else
        "future-head" if args == ("rev-parse", "HEAD") else
        "unreviewed-blob" if args[0] == "rev-parse" else ""
    ))
    with pytest.raises(RuntimeError, match="committed shared module differs"):
        install.preflight()


def test_committed_r2j_r2_rejects_non_descendant_head(monkeypatch, tmp_path):
    _fixture(monkeypatch, tmp_path)
    monkeypatch.setattr(
        install.subprocess, "run",
        lambda *args, **kwargs: SimpleNamespace(returncode=1),
    )
    with pytest.raises(RuntimeError, match="HEAD does not contain"):
        install.preflight()


def test_committed_r2j_r2_rejects_wrong_source_blob(monkeypatch, tmp_path):
    _fixture(monkeypatch, tmp_path)
    monkeypatch.setattr(install, "_git_bytes", lambda *args: b"unreviewed git content")
    with pytest.raises(RuntimeError, match="audited R2J-R2 Git blob changed"):
        install.preflight()


def test_committed_r2j_r2_accepts_already_installed_r2j_r3(monkeypatch, tmp_path):
    target, _ = _fixture(monkeypatch, tmp_path)
    target.write_bytes(install._insert_hook(target.read_bytes()))
    _, installed = install.preflight()
    assert installed is True

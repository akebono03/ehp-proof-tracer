"""Pure tests for the guarded R2H installer (without production modules)."""
from __future__ import annotations

from hashlib import sha1

import pytest

from phase171_r2h_prop22_cited_hopf.install import (
    ANCHOR_PROVIDER, ANCHOR_SOURCE, INSERT_PROVIDER, INSERT_SOURCE,
    full_functions, git_blob, patch_source,
)


BASE = ("def build_shared_typed_bridge():\n"
        "    if True:\n" + ANCHOR_SOURCE + "\n"
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n" + ANCHOR_PROVIDER + "\n")


def test_r2h_inserts_exactly_two_connections():
    patched = patch_source(BASE)
    assert patched.count(INSERT_SOURCE) == 1
    assert patched.count(INSERT_PROVIDER) == 1
    assert patched.index(ANCHOR_SOURCE) < patched.index(INSERT_SOURCE)


def test_r2h_preserves_crlf():
    patched = patch_source(BASE.replace("\n", "\r\n"))
    assert "\r\n" in patched
    assert patched.replace("\r\n", "\n") == patch_source(BASE)


def test_r2h_fails_closed_for_ambiguous_source_anchor():
    with pytest.raises(ValueError, match="anchors"):
        patch_source(BASE + ANCHOR_SOURCE)


def test_r2h_fails_closed_for_partial_integration():
    with pytest.raises(ValueError, match="partial"):
        patch_source(BASE.replace(ANCHOR_SOURCE, ANCHOR_SOURCE + "\n" + INSERT_SOURCE))


def test_r2h_extracts_two_whole_functions():
    functions = full_functions(patch_source(BASE))
    assert set(functions) == {"build_shared_typed_bridge", "shared_expansion_provider"}
    assert INSERT_SOURCE in functions["build_shared_typed_bridge"]
    assert INSERT_PROVIDER in functions["shared_expansion_provider"]


def test_git_blob_matches_standard_blob_calculation():
    data = b"hello\n"
    expected = sha1(b"blob 6\0hello\n").hexdigest()
    assert git_blob(data) == expected
    assert git_blob(b"hello\r\n") == expected

def _make_reviewed_git_fixture(tmp_path, monkeypatch, *, line_ending="\r\n"):
    """Create a real isolated Git repo, never touching the project worktree."""
    import subprocess
    from pathlib import Path

    import phase171_r2h_prop22_cited_hopf.install as installer

    def command(*args):
        output = subprocess.run(
            ["git", *args], cwd=tmp_path, capture_output=True,
            check=True, text=True, encoding="utf-8",
        )
        return output.stdout.strip()

    command("init", "-q")
    command("config", "user.email", "phase171@example.invalid")
    command("config", "user.name", "Phase171 Test")
    command("branch", "-M", "develop")
    target = tmp_path / "phase165_r52_r9_shared_math.py"
    committed_text = BASE.replace("\n", line_ending)
    target.write_bytes(committed_text.encode("utf-8"))
    command("add", "--", target.name)
    command("commit", "-qm", "reviewed baseline")
    monkeypatch.setattr(installer, "ROOT", tmp_path)
    monkeypatch.setattr(installer, "TARGET", target)
    monkeypatch.setattr(
        installer, "BASE_BLOB_SHA",
        command("rev-parse", "HEAD:" + target.name),
    )
    return installer, target, committed_text, command


def test_status_accepts_unchanged_crlf_git_blob(tmp_path, monkeypatch):
    installer, target, original, command = _make_reviewed_git_fixture(
        tmp_path, monkeypatch,
    )
    stage, before, after = installer.status()
    assert stage == "NEEDS_PATCH"
    assert before == original.encode("utf-8")
    assert after.decode("utf-8") == installer.patch_source(original)
    assert target.read_bytes() == before
    assert command("status", "--porcelain") == ""


def test_status_accepts_lf_worktree_from_crlf_commit(tmp_path, monkeypatch):
    installer, target, original, _ = _make_reviewed_git_fixture(
        tmp_path, monkeypatch,
    )
    # Reproduce a checkout whose text uses different line endings from Git.
    target.write_bytes(original.replace("\r\n", "\n").encode("utf-8"))
    stage, before, after = installer.status()
    assert stage == "NEEDS_PATCH"
    assert b"\r\n" not in after
    assert after != before


def test_status_recognizes_exact_patch_on_crlf_baseline(tmp_path, monkeypatch):
    installer, target, original, _ = _make_reviewed_git_fixture(
        tmp_path, monkeypatch,
    )
    target.write_bytes(installer.patch_source(original).encode("utf-8"))
    stage, before, after = installer.status()
    assert stage == "ALREADY_APPLIED"
    assert before == after == target.read_bytes()


def test_status_rejects_unreviewed_worktree_content(tmp_path, monkeypatch):
    installer, target, original, _ = _make_reviewed_git_fixture(
        tmp_path, monkeypatch,
    )
    edited = original.replace("def shared_expansion_provider():", "def intruder():")
    target.write_bytes(edited.encode("utf-8"))
    with pytest.raises(RuntimeError, match="unreviewed changes"):
        installer.status()
    assert target.read_bytes() == edited.encode("utf-8")


def test_status_rejects_unreviewed_committed_blob(tmp_path, monkeypatch):
    installer, target, original, command = _make_reviewed_git_fixture(
        tmp_path, monkeypatch,
    )
    target.write_bytes((original + "# new change\r\n").encode("utf-8"))
    command("add", "--", target.name)
    command("commit", "-qm", "unreviewed production change")
    with pytest.raises(RuntimeError, match="reviewed baseline"):
        installer.status()

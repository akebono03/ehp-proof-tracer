"""The R3Z assertion correction must be exact, semantic, and idempotent."""
from __future__ import annotations

import ast

import pytest

from phase171_closeout_r1r1_r3z_semantic_guard.install import (
    NEW, OLD, REVIEWED, REVIEWED_BLOB, git_blob, normalized,
    preserve_format, transform,
)


def test_reviewed_baseline_is_the_github_blob():
    reviewed = REVIEWED.read_bytes()
    assert git_blob(reviewed) == REVIEWED_BLOB
    assert reviewed.count(OLD.encode("utf-8")) == 1


def test_only_one_legacy_assertion_is_replaced_and_module_parses():
    reviewed = REVIEWED.read_bytes()
    actual = transform(reviewed)
    assert actual == reviewed.replace(OLD.encode("utf-8"), NEW.encode("utf-8"), 1)
    ast.parse(actual.decode("utf-8"))
    assert b"assert len(model.steps) == 28" not in actual
    assert b"model.steps is proof.proven_steps" in actual
    assert actual.count(b"def test_r3z_general_higher_eta_is_reference_only") == 1


def test_unreviewed_source_is_rejected():
    with pytest.raises(RuntimeError, match="differs from reviewed baseline"):
        transform(REVIEWED.read_bytes().replace(b"len(model.steps)", b"len(other.steps)"))


def test_preserves_windows_crlf_and_utf8_bom():
    reviewed = REVIEWED.read_bytes()
    windows = b"\xef\xbb\xbf" + reviewed.replace(b"\n", b"\r\n")
    patched = preserve_format(windows, transform(windows))
    assert patched.startswith(b"\xef\xbb\xbf")
    assert b"\r\n" in patched
    assert b"\n" not in patched.replace(b"\r\n", b"")
    assert normalized(patched) == transform(reviewed)


def test_git_porcelain_retains_leading_status_column(tmp_path, monkeypatch):
    import subprocess
    from phase171_closeout_r1r1_r3z_semantic_guard import install

    def invoke(*args):
        subprocess.run(["git", "-C", str(tmp_path), *args],
                       check=True, capture_output=True)

    invoke("init", "-q")
    invoke("config", "user.email", "phase171@example.org")
    invoke("config", "user.name", "Phase 171 Test")
    target = tmp_path / "test.txt"
    target.write_text("before\n", encoding="utf-8")
    invoke("add", "test.txt")
    invoke("commit", "-qm", "baseline")
    target.write_text("after\n", encoding="utf-8")
    monkeypatch.setattr(install, "ROOT", tmp_path)
    assert install.git("status", "--porcelain=v1", "--untracked-files=no") == " M test.txt"

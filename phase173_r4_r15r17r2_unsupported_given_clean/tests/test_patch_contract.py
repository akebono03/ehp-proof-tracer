"""Strict single-anchor patch and AST contract, independent of the repository."""
from __future__ import annotations

import ast

import pytest

from phase173_r4_r15r17r2_unsupported_given_clean.patch import OLD, NEW, transform
from phase173_r4_r15r17r2_unsupported_given_clean import install as installer


def test_patch_replaces_only_one_verified_fallback() -> None:
    source = (
        "def example():\n"
        "    while True:\n"
        "        if True:\n"
        "            if True:\n"
        "                if sentence is not None:\n"
        "                    statement_text = sentence\n"
        + OLD
    )
    transformed = transform(source)
    assert transformed == source.replace(OLD, NEW)
    assert "type(statement).__name__" not in transformed
    assert "if latex is None or fallback is not None:" in transformed
    assert "                    continue\n" in transformed
    assert ast.parse(transformed)


def test_reapply_or_unreviewed_source_fails_closed() -> None:
    source = (
        "def example():\n"
        "    while True:\n"
        "        if True:\n"
        "            if True:\n"
        "                if sentence is not None:\n"
        "                    statement_text = sentence\n"
        + OLD
    )
    patched = transform(source)
    with pytest.raises(RuntimeError, match="unreviewed renderer or already installed"):
        transform(patched)
    with pytest.raises(RuntimeError, match="unreviewed renderer or already installed"):
        transform(source + OLD)


def test_no_named_generator_or_dimension_branch_added() -> None:
    assert "sphere_dimension" not in NEW
    assert "group_dimension" not in NEW
    assert "ProofSearchStatus.COMPLETE" not in NEW
    assert "citation" not in NEW.lower()


def test_installer_restore_preserves_original_and_git_index(tmp_path, monkeypatch) -> None:
    target = tmp_path / "renderer.py"
    target.write_bytes(b"original renderer\n")
    monkeypatch.setattr(installer, "TARGET_PATH", target)
    monkeypatch.setattr(installer, "STATE", tmp_path / "state.json")
    monkeypatch.setattr(installer, "BACKUP", tmp_path / "backup.bin")
    monkeypatch.setattr(installer, "git", lambda *args: "index-unchanged")
    installer.install((b"original renderer\n", b"updated renderer\n"),
                      "index-unchanged")
    assert target.read_bytes() == b"updated renderer\n"
    assert installer.STATE.is_file()
    installer.restore()
    assert target.read_bytes() == b"original renderer\n"
    assert not installer.STATE.exists()
    assert not installer.BACKUP.exists()


def test_restorer_refuses_overwriting_subsequent_user_edit(tmp_path, monkeypatch) -> None:
    target = tmp_path / "renderer.py"
    target.write_bytes(b"original renderer\n")
    monkeypatch.setattr(installer, "TARGET_PATH", target)
    monkeypatch.setattr(installer, "STATE", tmp_path / "state.json")
    monkeypatch.setattr(installer, "BACKUP", tmp_path / "backup.bin")
    monkeypatch.setattr(installer, "git", lambda *args: "index-unchanged")
    installer.install((b"original renderer\n", b"updated renderer\n"),
                      "index-unchanged")
    target.write_bytes(b"subsequent user change\n")
    with pytest.raises(RuntimeError, match="user modifications"):
        installer.restore()
    assert target.read_bytes() == b"subsequent user change\n"

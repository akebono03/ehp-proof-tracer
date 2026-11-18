"""Whole-function installer guard, never partial unscoped text edits."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase175_r4r11_signed_eta_torsion_public import installer


def sample_code() -> str:
    return (
        "def before():\n    return 1\n\n"
        "def shared_expansion_provider(bridge):\n"
        + installer.ANCHOR
        + "    return extra_providers\n\n"
        + "def after():\n    return 2\n"
    )


def test_one_complete_function_patched(monkeypatch: pytest.MonkeyPatch) -> None:
    content = sample_code()
    monkeypatch.setattr(installer, "BASE_WORKING_BLOB", installer.git_blob_sha(content.encode()))
    updated, after, base = installer.function_replacement(content)
    assert installer.ADDITION in after
    assert base == content
    assert updated.count(installer.ADDITION) == 1
    assert "def before():\n    return 1" in updated
    assert "def after():\n    return 2" in updated
    ast.parse(updated)


def test_installer_idempotent_and_exact_base(monkeypatch: pytest.MonkeyPatch) -> None:
    content = sample_code()
    monkeypatch.setattr(installer, "BASE_WORKING_BLOB", installer.git_blob_sha(content.encode()))
    once = installer.function_replacement(content)[0]
    twice = installer.function_replacement(once)[0]
    assert once == twice
    with pytest.raises(RuntimeError, match="UNREVIEWED_BASE_SOURCE"):
        installer.function_replacement(once.replace("return 1", "return 3"))


def test_anchor_or_function_change_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    content = sample_code()
    monkeypatch.setattr(installer, "BASE_WORKING_BLOB", installer.git_blob_sha(content.encode()))
    with pytest.raises(RuntimeError, match="ANCHOR_CHANGED"):
        installer.function_replacement(content.replace("build_cited_58_prop25_provider", "other"))
    with pytest.raises(RuntimeError, match="FUNCTION_NOT_UNIQUE"):
        installer.function_replacement(content + content)


def test_dry_run_writes_complete_function_but_not_production(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    path = root / installer.TARGET
    initial = sample_code()
    path.write_text(initial, encoding="utf-8")
    monkeypatch.setattr(installer, "BASE_WORKING_BLOB", installer.git_blob_sha(initial.encode()))
    monkeypatch.setattr(installer, "git", lambda root, *args: installer.REVIEWED_COMMITTED_BLOBS[0])
    result = installer.install(root, dry_run=True, output=tmp_path / "output")
    assert result["patch_required"] is True
    assert result["patch_applied"] is False
    assert path.read_text(encoding="utf-8") == initial
    assert "def shared_expansion_provider" in (
        tmp_path / "output" / "shared_expansion_provider_FULL_AFTER.py"
    ).read_text(encoding="utf-8")


def test_real_install_only_one_function(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    path = root / installer.TARGET
    initial = sample_code()
    path.write_text(initial, encoding="utf-8")
    monkeypatch.setattr(installer, "BASE_WORKING_BLOB", installer.git_blob_sha(initial.encode()))
    monkeypatch.setattr(installer, "git", lambda root, *args: installer.REVIEWED_COMMITTED_BLOBS[0])
    result = installer.install(root, dry_run=False, output=tmp_path / "output")
    assert result["patch_applied"] is True
    installed = path.read_text(encoding="utf-8")
    assert installer.ADDITION in installed
    assert "def before():\n    return 1" in installed
    assert "def after():\n    return 2" in installed
    again = installer.install(root, dry_run=False, output=tmp_path / "output")
    assert again["patch_required"] is False

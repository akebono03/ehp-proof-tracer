"""Byte-for-byte minimal production patch contract (no live code required)."""
from __future__ import annotations

import ast

import pytest

from phase174_r3_r7_r14_public_annihilator_connection.patch import (
    EXPECTED_BLOB, PROVIDER_ANCHOR, PROVIDER_REPLACEMENT,
    SOURCE_ANCHOR, SOURCE_REPLACEMENT, TARGET, git_blob_sha,
    transform_source,
)


def base_source() -> str:
    return ("from __future__ import annotations\n"
            "def build_shared_typed_bridge():\n"
            "    if True:\n"
            + SOURCE_ANCHOR + "\n"
            "def shared_expansion_provider():\n"
            "    def expand(goal):\n"
            + PROVIDER_ANCHOR + "\n")


def test_two_stable_anchors_patch_once() -> None:
    new = transform_source(base_source())
    assert new.count(SOURCE_REPLACEMENT) == 1
    assert new.count(PROVIDER_REPLACEMENT) == 1
    assert "phase174_r3_r7_r13_cited_annihilator_bridge.registry" in new
    assert "phase174_r3_r7_r12_toda59_annihilator_source.rule" in new
    assert "expand_cited_annihilator_specialization(goal, tuple(available))" in new
    assert isinstance(ast.parse(new), ast.Module)


@pytest.mark.parametrize("replace", ("missing_source", "missing_provider", "duplicate_source", "duplicate_provider"))
def test_missing_or_duplicated_anchor_rejected(replace: str) -> None:
    src = base_source()
    if replace == "missing_source":
        src = src.replace(SOURCE_ANCHOR, "pass")
    if replace == "missing_provider":
        src = src.replace(PROVIDER_ANCHOR, "pass")
    if replace == "duplicate_source":
        src += "\n" + SOURCE_ANCHOR
    if replace == "duplicate_provider":
        src += "\n" + PROVIDER_ANCHOR
    with pytest.raises(RuntimeError, match="exactly one"):
        transform_source(src)


def test_reapplication_does_not_duplicate_source_registration() -> None:
    with pytest.raises(RuntimeError):
        transform_source(transform_source(base_source()))


def test_only_two_general_patches_are_inserted() -> None:
    new = transform_source(base_source())
    assert new.replace(SOURCE_REPLACEMENT, SOURCE_ANCHOR).replace(
        PROVIDER_REPLACEMENT, PROVIDER_ANCHOR
    ) == base_source()
    assert "TodaPrimaryGroupZeroStatement" not in new
    assert "π₁₂" not in new
    assert "GIVEN" not in new
    assert "n == 6" not in new


def test_pinned_sha_and_git_blob_format() -> None:
    assert len(EXPECTED_BLOB) == 40
    assert str(TARGET) == "phase165_r52_r9_shared_math.py"
    sha = git_blob_sha(b"abc\n")
    assert len(sha) == 40
    assert sha != git_blob_sha(b"abc\r\n")


def test_line_endings_are_preserved_and_mixed_rejected(monkeypatch) -> None:
    from phase174_r3_r7_r14_public_annihilator_connection import patch
    src = base_source().encode("utf-8")
    monkeypatch.setattr(patch, "EXPECTED_BLOB", patch.git_blob_sha(src))
    assert patch.expected_patched_bytes(src).endswith(b"\n")
    crlf = src.replace(b"\n", b"\r\n")
    assert patch.expected_patched_bytes(crlf).endswith(b"\r\n")
    assert b"\r\n" not in patch.expected_patched_bytes(src)
    with pytest.raises(RuntimeError, match="Mixed"):
        patch.expected_patched_bytes(crlf + b"bad\n")


def test_modified_functions_export_contains_entire_bodies(monkeypatch, tmp_path) -> None:
    from phase174_r3_r7_r14_public_annihilator_connection import patch
    src = base_source().encode("utf-8")
    monkeypatch.setattr(patch, "EXPECTED_BLOB", patch.git_blob_sha(src))
    (tmp_path / patch.TARGET).write_bytes(src)
    folder = tmp_path / "phase174_r3_r7_r14_public_annihilator_connection"
    folder.mkdir()
    full = patch.export_modified_functions(tmp_path, dry_run=True).read_text(encoding="utf-8")
    assert "def build_shared_typed_bridge():" in full
    assert "def shared_expansion_provider():" in full
    assert "expand_cited_annihilator_specialization" in full
    assert "build_isolated_toda59_annihilator_bridge" in full
    assert (tmp_path / patch.TARGET).read_bytes() == src

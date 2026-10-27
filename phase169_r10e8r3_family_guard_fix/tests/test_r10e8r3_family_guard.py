"""Regression tests: real R10D2 uses source.family_id and statement.family_id."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase169_r10e8_hyoujigen_generic_suspension import patch as original
from phase169_r10e8r3_family_guard_fix.patch import (
    OLD_REFERENCE,
    NEW_REFERENCE,
    apply_guarded_r3_patch,
    transformed_sources_r3,
)


def _minimal_reviewed_sources() -> tuple[str, str]:
    family = (
        "from __future__ import annotations\n"
        "from proof import (\n"
        "    ProofRule,\n"
        ")\n"
        "\nROOT = 'example'\n"
        "def canonical_member(source):\n"
        "    return source.family_id not in "
        "{record.family_id for record in SOURCE_RECORDS}\n"
        "def cited_family_reference_sentence(statement):\n"
        "    return statement.family_id not in "
        "{record.family_id for record in SOURCE_RECORDS}\n"
    )
    shared = (
        "from __future__ import annotations\n"
        "def build_shared_typed_bridge():\n"
        "        sources = sources + (build_cited_stable_family_definitions(),)\n"
    )
    return family, shared


def test_r10e8r3_exact_distinct_anchors_not_two_source_occurrences():
    family, shared = _minimal_reviewed_sources()
    assert family.count(original.OLD_MEMBER) == 1
    assert family.count(OLD_REFERENCE) == 1
    updated_family, updated_shared = transformed_sources_r3(family, shared)
    assert updated_family.count(original.NEW_MEMBER) == 1
    assert updated_family.count(NEW_REFERENCE) == 1
    assert updated_family.count(original.NEW_IMPORT) == 1
    assert "build_cited_chapter_vi_family_definitions" in updated_shared
    assert "def canonical_member" in updated_family
    assert "def cited_family_reference_sentence" in updated_family


def test_r10e8r3_current_repository_guard_matches_actual_r10d2_file():
    root = Path(__file__).resolve().parents[2]
    file = root / "phase169_r10d2_general_family_definition" / "family_citation.py"
    if not file.is_file():
        pytest.skip("complete repository checkout is required")
    source = file.read_text(encoding="utf-8")
    if "CHAPTER_VI_SOURCE_RECORDS" not in source:
        assert source.count(original.OLD_MEMBER) == 1
        assert source.count(OLD_REFERENCE) == 1
    else:
        assert source.count(original.NEW_MEMBER) == 1
        assert source.count(NEW_REFERENCE) == 1


def test_r10e8r3_second_guard_is_not_silently_omitted():
    family, shared = _minimal_reviewed_sources()
    family = family.replace(OLD_REFERENCE, "statement.family_id == -1")
    with pytest.raises(RuntimeError, match="distinct family guards"):
        transformed_sources_r3(family, shared)


def test_r10e8r3_rejects_duplicate_guard_outside_expected_function():
    family, shared = _minimal_reviewed_sources()
    family += "def unrelated(source):\n    return " + original.OLD_MEMBER + "\n"
    with pytest.raises(RuntimeError, match="distinct family guards"):
        transformed_sources_r3(family, shared)


def test_r10e8r3_rejects_already_patched_source():
    family, shared = _minimal_reviewed_sources()
    changed_family, changed_shared = transformed_sources_r3(family, shared)
    with pytest.raises(RuntimeError, match="distinct family guards"):
        transformed_sources_r3(changed_family, changed_shared)


@pytest.mark.parametrize("style", ["\n", "\r\n"])
def test_r10e8r3_file_application_preserves_line_endings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, style: str,
):
    family, shared = _minimal_reviewed_sources()
    family_path = tmp_path / "family.py"
    shared_path = tmp_path / "shared.py"
    out = tmp_path / "output"
    family_path.write_bytes(family.replace("\n", style).encode("utf-8"))
    shared_path.write_bytes(shared.replace("\n", style).encode("utf-8"))
    monkeypatch.setattr(original, "FAMILY", family_path)
    monkeypatch.setattr(original, "SHARED", shared_path)
    monkeypatch.setattr(original, "OUTPUT", out)
    apply_guarded_r3_patch()
    assert b"CHAPTER_VI_SOURCE_RECORDS" in family_path.read_bytes()
    for file in (family_path, shared_path):
        data = file.read_bytes()
        if style == "\r\n":
            assert b"\r\n" in data
            assert b"\n" not in data.replace(b"\r\n", b"")
        else:
            assert b"\r\n" not in data
    for name in ("family_citation_IMPORTS_FULL.py", "canonical_member_FULL.py",
                 "cited_family_reference_sentence_FULL.py",
                 "build_shared_typed_bridge_FULL.py"):
        assert (out / name).is_file()


def test_r10e8r3_malformed_source_preserves_original_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
):
    family, shared = _minimal_reviewed_sources()
    family_path = tmp_path / "family.py"
    shared_path = tmp_path / "shared.py"
    original_family = family.encode("utf-8")
    original_shared = shared.replace("\n", "\r\n").encode("utf-8")
    family_path.write_bytes(original_family)
    shared_path.write_bytes(original_shared)
    monkeypatch.setattr(original, "FAMILY", family_path)
    monkeypatch.setattr(original, "SHARED", shared_path)
    monkeypatch.setattr(original, "OUTPUT", tmp_path / "output")
    family_path.write_bytes(original_family.replace(
        OLD_REFERENCE.encode("utf-8"), b"broken_reference_guard",
    ))
    corrupted = family_path.read_bytes()
    with pytest.raises(RuntimeError, match="distinct family guards"):
        apply_guarded_r3_patch()
    assert family_path.read_bytes() == corrupted
    assert shared_path.read_bytes() == original_shared

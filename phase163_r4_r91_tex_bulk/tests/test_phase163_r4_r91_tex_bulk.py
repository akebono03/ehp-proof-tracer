import copy
import hashlib
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase163_r4_r91_tex_bulk import (
    CHAPTER_FILES,
    extract_chapter,
    extract_five_chapters,
    integrate_source_catalog,
    write_outputs,
)
from phase163_r4_registry_bridge import build_registry_bridge
from unified_statement_registry import AssertionOrigin

ROOT = Path(__file__).resolve().parents[2]


def sample_chapters(tmp_path):
    text = (
        "\\begin{proposition}\\label{prop:1.1}\n"
        "A \\begin{equation}\\label{1.2} B \\end{equation}\n"
        "\\end{proposition}\n"
        "\\begin{equation}\\label{1.3} C \\end{equation}\n"
    )
    for i, filename in enumerate(CHAPTER_FILES, 1):
        (tmp_path / filename).write_text(text.replace("1.", f"{i}."), encoding="utf-8")


def test_nested_equation_is_not_separate_reference(tmp_path):
    sample_chapters(tmp_path)
    rows = extract_chapter(tmp_path / CHAPTER_FILES[0], 1)
    assert len(rows) == 2
    assert [x["locator"] for x in rows] == ["Proposition 1.1", "(1.3)"]


def test_five_chapter_publication_order(tmp_path):
    sample_chapters(tmp_path)
    catalog = extract_five_chapters(tmp_path)
    assert catalog["record_count"] == 10
    assert [x["publication_position"] for x in catalog["records"]] == list(range(1, 11))
    assert [x["chapter"] for x in catalog["records"]] == sorted(x["chapter"] for x in catalog["records"])


def test_source_only_bridge_and_reused_reference(tmp_path):
    sample_chapters(tmp_path)
    catalog = extract_five_chapters(tmp_path)
    bridge = build_registry_bridge(components_by_reference={}, theorem_facts=SimpleNamespace(entries=()))
    registry, report = integrate_source_catalog(catalog, bridge=bridge)
    assert report["source_assertion_added_count"] == 10
    for row in catalog["records"]:
        assertion = registry.assertion(row["source_id"])
        assert assertion.origin is AssertionOrigin.SOURCE_ARCHIVE
        assert assertion.content["proof_eligible"] is False
        assert assertion.available_after_position is None


def test_tampered_text_refused(tmp_path):
    sample_chapters(tmp_path)
    catalog = extract_five_chapters(tmp_path)
    catalog["records"][0]["source_text"] += "modified"
    with pytest.raises(ValueError, match="integrity"):
        integrate_source_catalog(catalog, bridge=build_registry_bridge(
            components_by_reference={}, theorem_facts=SimpleNamespace(entries=())))


def test_missing_chapter_refused(tmp_path):
    with pytest.raises(FileNotFoundError):
        extract_five_chapters(tmp_path)


def test_unlabelled_preserved_with_review_flag(tmp_path):
    f = tmp_path / CHAPTER_FILES[0]
    f.write_text("\\begin{lemma} statement \\end{lemma}", encoding="utf-8")
    rows = extract_chapter(f, 1)
    assert len(rows) == 1
    assert rows[0]["review_needed"] is True
    assert rows[0]["locator"].startswith("UNLABELED")


def test_write_outputs(tmp_path):
    source = tmp_path / "src"
    source.mkdir()
    sample_chapters(source)
    catalog = extract_five_chapters(source)
    _, summary = integrate_source_catalog(catalog, bridge=build_registry_bridge(
        components_by_reference={}, theorem_facts=SimpleNamespace(entries=())))
    write_outputs(catalog, summary, tmp_path / "out")
    assert (tmp_path / "out" / "source_catalog.json").is_file()
    assert "10 件" in (tmp_path / "out" / "report.md").read_text(encoding="utf-8")


def test_repository_source_extraction():
    catalog = extract_five_chapters(ROOT / "sources" / "toda")
    assert catalog["chapters"] == 5
    assert catalog["record_count"] > 30
    assert all(row["source_text"] for row in catalog["records"])
    assert all(row["status"] == "SOURCE_ONLY" for row in catalog["records"])

"""Standalone TeX evidence scanner tests: text hits never become proof leaves."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase173_r4_r15r5_family_source_frontier.source_scan import (
    scan_adopted_toda_sources,
    scan_text,
)


def test_delta_definition_is_only_an_unreviewed_text_hit() -> None:
    hits = scan_text(r"\delta_n:=E^{n-3}\delta_3", family_id=88,
                     relative_path="example.tex")
    assert len(hits) == 1
    assert hits[0]["kind"] == "indexed_definition"
    assert hits[0]["source_reviewed"] is False


def test_bar_kappa_definition_is_only_an_unreviewed_text_hit() -> None:
    hits = scan_text(r"\bar{\kappa}_n:=E^{n-7}\bar{\kappa}_7", family_id=56,
                     relative_path="example.tex")
    assert len(hits) == 1
    assert hits[0]["source_reviewed"] is False


def test_database_metadata_text_never_matches_definition() -> None:
    for family_id, text in ((56, r"\bar{\kappa}_{14}"),
                            (88, r"\Delta_3\sigma_{27}")):
        assert scan_text(text, family_id=family_id,
                         relative_path="example.tex") == ()


def test_unexpected_family_refused() -> None:
    with pytest.raises(ValueError, match="Unreviewed family ID"):
        scan_text(r"\delta_n:=E\delta_3", family_id=999,
                  relative_path="example.tex")


def test_scan_existing_local_chapter_returns_provenance_not_proof(tmp_path: Path) -> None:
    directory = tmp_path / "sources" / "toda"
    directory.mkdir(parents=True)
    (directory / "Toda_99_2.tex").write_text(
        r"\delta_n:=E^{n-3}\delta_3" + "\n", encoding="utf-8",
    )
    result = scan_adopted_toda_sources(tmp_path, family_id=88)
    assert result["family_id"] == 88
    assert len(result["candidate_text_hits"]) == 1
    assert result["source_definition_certified"] is False
    assert result["new_given_created"] is False
    assert len(result["source_files"][0]["sha256"]) == 64

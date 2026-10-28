"""Tests for pure read-only Definition candidate discovery and metadata guards."""
from __future__ import annotations

import csv
from pathlib import Path

import pytest

from phase169_r10eo_r1_definition_audit.audit import (
    classify_source, literal_definition_candidates, normalize_tex, read_metadata,
)


def sample_row(*, identity: int = 16, display: str = "ζ", n: int = 5,
               k: int = 11, latex: str = r"\zeta") -> dict:
    return {
        "id": identity, "display": display, "kinds": 0,
        "k": k, "n": n, "latex": latex,
        "stable": "", "stable_orders": "",
    }


def test_r10eo_literal_zeta_definition_detected_as_untrusted_candidate():
    tex = ("\\paragraph{v). The elements zeta.}\n"
           "\\zeta_{n}:=E^{\\,n-5}\\zeta_{5}\\quad(n\\ge5)\n")
    found = literal_definition_candidates(sample_row(), tex, source_id="chapter_vi")
    assert len(found) == 1
    assert found[0]["source_id"] == "chapter_vi"
    assert found[0]["line"] == 2
    assert found[0]["classification"] == "TEXT_MATCH_CANDIDATE_NOT_AUTHORIZED"
    assert classify_source(sample_row(), set(), found) == "TEXT_MATCH_REQUIRES_INDEPENDENT_REVIEW"


def test_r10eo_metadata_without_source_or_citation_is_not_evidence():
    row = sample_row()
    assert literal_definition_candidates(row, r"\zeta_n \in \pi_{n+11}^n", source_id="chapter_vi") == []
    assert classify_source(row, set(), []) == "NO_REGISTERED_CITED_DEFINITION"
    assert classify_source(row, {16}, []) == "REGISTERED_CITED_DEFINITION"


def test_r10eo_wrong_stem_symbol_or_base_cannot_make_verified_clause():
    correct = r"\zeta_n:=E^{n-5}\zeta_5"
    assert literal_definition_candidates(sample_row(n=6), correct, source_id="chapter_vi") == []
    assert literal_definition_candidates(sample_row(latex=r"\sigma"), correct, source_id="chapter_vi") == []
    assert literal_definition_candidates(sample_row(), r"\zeta_n:=E^{n-6}\zeta_5", source_id="chapter_vi") == []


def test_r10eo_chapter_vi_existing_mu_and_barnu_are_generic():
    mu = sample_row(identity=12, display="μ", n=3, k=9, latex=r"\mu")
    nu = sample_row(identity=11, display="ν̅", n=6, k=8, latex=r"\bar{\nu}")
    assert len(literal_definition_candidates(mu, r"\mu_{n}:=E^{\,n-3}\mu_{3}", source_id="chapter_vi")) == 1
    assert len(literal_definition_candidates(nu, r"\overline{\nu}_n:=E^{\,n-6}\overline{\nu}_6", source_id="chapter_vi")) == 1
    assert normalize_tex(r"\zeta_{n}:=E^{\,n-5}\zeta_{5}") == r"\zeta_n:=E^{n-5}\zeta_5"


def test_r10eo_only_kinds_zero_can_supply_a_definition_candidate():
    row = sample_row()
    row["kinds"] = 1
    assert literal_definition_candidates(row, r"\zeta_n:=E^{n-5}\zeta_5", source_id="chapter_vi") == []
    row["kinds"] = 0
    row["id"] = 0
    assert literal_definition_candidates(row, r"\zeta_n:=E^{n-5}\zeta_5", source_id="chapter_vi") == []


def test_r10eo_csv_schema_is_required(tmp_path: Path):
    source = tmp_path / "broken.csv"
    source.write_text("id,display,kinds,k,n,latex\n16,ζ,0,11,5,\\zeta\n", encoding="utf-8")
    with pytest.raises(ValueError, match="required columns"):
        read_metadata(source)


def test_r10eo_duplicate_generator_id_is_rejected(tmp_path: Path):
    source = tmp_path / "duplicate.csv"
    with source.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("id", "display", "kinds", "k", "n", "orders", "latex", "stable", "stable_orders"))
        writer.writerow((16, "ζ", 0, 11, 5, 8, r"\zeta", "", ""))
        writer.writerow((16, "ζ", 0, 11, 5, 8, r"\zeta", "", ""))
    with pytest.raises(ValueError, match="duplicate generator ID"):
        read_metadata(source)

"""Focused tests for source-neutral literal Definition indexing only."""
from __future__ import annotations

from dataclasses import replace

from phase169_r10b_registered_stable_family_binding.family_registry import (
    RegisteredStableFamily,
)
from phase169_r10eo_r2_definition_index.definition_index import (
    expected_formula,
    mask_tex_comments,
    normalized_tex,
    occurrences_for_family,
)


def family(*, family_id: int = 16, stem: int = 11, minimum_n: int = 5,
           latex: str = r"\zeta") -> RegisteredStableFamily:
    return RegisteredStableFamily(
        family_id=family_id,
        display="ζ",
        symbol_family=latex,
        stem=stem,
        minimum_n=minimum_n,
        latex=latex,
    )


def locate(item: RegisteredStableFamily, text: str):
    return occurrences_for_family(
        item, text, source_id="chapter_vi",
        source_path="sources/toda/Toda_06_2.tex",
    )


def test_r10eo_r2_one_exact_zeta_formula_not_two_overlapping_windows():
    source = (r"\paragraph{v). The elements \(\zeta_n\).}" + "\n"
              + r"\zeta_5:=x" + "\n"
              + r"\zeta_{n}:=E^{\,n-5}\zeta_{5}\quad(n\ge5),"
              + "\n" + r"\zeta:=E^{\infty}\zeta_5" + "\n")
    items = locate(family(), source)
    assert len(items) == 1
    assert items[0].line == 3
    assert items[0].classification == "TEXT_ONLY_NOT_CITED"
    assert items[0].preceding_paragraph is not None
    assert items[0].source_sha256 and len(items[0].source_sha256) == 64


def test_r10eo_r2_generator_agnostic_symbols():
    for ident, tex, minimum_n in ((16, r"\zeta", 5),
                                  (4, r"\nu", 4),
                                  (9, r"\sigma", 8),
                                  (12, r"\mu", 3)):
        item = family(family_id=ident, minimum_n=minimum_n, latex=tex)
        statement = rf"{tex}_{{n}} := E^{{\,n-{minimum_n}}}{tex}_{{{minimum_n}}}"
        found = locate(item, statement)
        assert len(found) == 1
        assert found[0].family_id == ident
        assert found[0].minimum_n == minimum_n


def test_r10eo_r2_barnu_overline_spelling_normalizes():
    item = family(family_id=11, minimum_n=6, latex=r"\bar{\nu}")
    found = locate(item, r"\overline{\nu}_n:=E^{\,n-6}\overline{\nu}_6")
    assert len(found) == 1


def test_r10eo_r2_wrong_base_or_symbol_fails_closed():
    item = family()
    assert locate(item, r"\zeta_n:=E^{n-6}\zeta_5") == ()
    assert locate(item, r"\zeta_n:=E^{n-5}\sigma_5") == ()
    assert locate(replace(item, minimum_n=6), r"\zeta_n:=E^{n-5}\zeta_5") == ()


def test_r10eo_r2_repeated_exact_definitions_remain_ambiguous():
    source = r"\zeta_n:=E^{n-5}\zeta_5" + "\n" + r"\zeta_n:=E^{n-5}\zeta_5"
    found = locate(family(), source)
    assert len(found) == 2
    assert found[0].start_offset != found[1].start_offset


def test_r10eo_r2_comments_do_not_create_candidates():
    source = "% " + r"\zeta_n:=E^{n-5}\zeta_5" + "\n"
    assert locate(family(), source) == ()
    assert r"\zeta_n" not in mask_tex_comments(source)


def test_r10eo_r2_symbol_index_metadata_stays_unauthorized():
    item = family()
    source = r"\zeta_n:=E^{n-5}\zeta_5"
    found = locate(item, source)
    assert len(found) == 1
    assert "GIVEN" not in found[0].classification
    assert found[0].classification == "TEXT_ONLY_NOT_CITED"
    assert expected_formula(item) == normalized_tex(source)


def test_r10eo_r2_comments_cannot_override_real_source():
    source = ("% " + r"\zeta_n:=E^{n-6}\zeta_5" + "\n"
              + r"\zeta_n:=E^{n-5}\zeta_5" + "\n")
    found = locate(family(), source)
    assert len(found) == 1
    assert found[0].line == 2

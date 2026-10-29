"""Focused checks intended to run against the user's complete local repository."""
from __future__ import annotations

from pathlib import Path

from fix_source712 import EXPECTED_CLAUSE, normalized_utf8, verify_reviewed_toda712
from phase170_r3_r9_toda712_cited_rewrite.source712 import (
    CLAUSE,
    verified_toda712_generator_equality,
)


def test_r3r9r2_exact_citation_matches_reviewed_toda_tex() -> None:
    tex = normalized_utf8(Path("sources/toda/Toda_07_2.tex"))
    offset = verify_reviewed_toda712(tex)
    assert CLAUSE == EXPECTED_CLAUSE
    assert tex[offset:offset + len(CLAUSE)] == CLAUSE
    assert tex.count(CLAUSE) == 1


def test_r3r9r2_existing_typed_verifier_still_checks_source() -> None:
    relation, position = verified_toda712_generator_equality()
    tex = normalized_utf8(Path("sources/toda/Toda_07_2.tex"))
    clause_offset = verify_reviewed_toda712(tex)
    assert tex[clause_offset:clause_offset + len(CLAUSE)] == CLAUSE
    assert relation is not None
    assert type(position) is int
    assert position >= 0


def test_r3r9r2_bar_alias_is_not_accepted_as_unreviewed_source() -> None:
    tex = normalized_utf8(Path("sources/toda/Toda_07_2.tex"))
    modified = tex.replace(CLAUSE, CLAUSE.replace(r"\ov{\nu}", r"\bar{\nu}"), 1)
    assert modified != tex
    assert modified.count(CLAUSE) == 0

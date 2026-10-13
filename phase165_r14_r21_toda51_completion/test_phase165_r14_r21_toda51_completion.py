from pathlib import Path
import pytest
from phase165_r14_r21_toda51_completion import (
    CLAUSE_KEYS, complete_toda51_source, diagonal_specializations,
)

SOURCE = Path(__file__).with_name("toda_51_complete.tex").read_text(encoding="utf-8")

def test_six_clauses_share_existing_locator():
    source = complete_toda51_source(SOURCE)
    assert tuple(c.key for c in source.clauses) == CLAUSE_KEYS
    assert all(c.reference_locator == "(5.1)" for c in source.clauses)

def test_adjacent_three_clauses_preserved():
    source = complete_toda51_source(SOURCE)
    assert r"\pi^{n}_{n}" in source.clauses[3].source_tex
    assert r"G_0=" in source.clauses[4].source_tex
    assert r"E^{\infty}" in source.clauses[5].source_tex

def test_missing_adjacent_display_rejected():
    with pytest.raises(ValueError):
        complete_toda51_source(SOURCE.split(r"\[")[0])

def test_missing_one_clause_rejected():
    with pytest.raises(ValueError):
        complete_toda51_source(SOURCE.replace(r"\iota=E^{\infty}\iota_n", ""))

def test_stray_remote_display_rejected():
    with pytest.raises(ValueError):
        complete_toda51_source(SOURCE.replace(r"\end{equation}", r"\end{equation} unrelated text"))

def test_diagonal_specialization_is_typed():
    a, b = diagonal_specializations(complete_toda51_source(SOURCE))
    assert a.lhs.group_dimension == 1 and b.lhs.group_dimension == 2
    assert a.rhs.generator.generator.index == 1
    assert b.rhs.generator.generator.index == 2

def test_empty_source_rejected():
    with pytest.raises(ValueError):
        complete_toda51_source("")

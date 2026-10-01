from __future__ import annotations

import ast
from pathlib import Path

import audit_phase155_r2 as r2


def _assert_node(source: str) -> ast.Assert:
    tree = ast.parse(source)
    function = tree.body[0]
    assert isinstance(function, ast.FunctionDef)
    assertion = function.body[0]
    assert isinstance(assertion, ast.Assert)
    return assertion


def test_positive_membership_extracts_literal():
    assertion = _assert_node(
        'def test_x():\n    assert "まず、結果を得る。" in rendered\n'
    )
    assert r2._positive_literal_membership(assertion) == [
        ("まず、結果を得る。", 2)
    ]


def test_japanese_prose_punctuation_is_detected():
    assert r2._contains_japanese_prose_punctuation("まず、結果を得る。")
    assert not r2._contains_japanese_prose_punctuation("まず, 結果を得る.")
    assert not r2._contains_japanese_prose_punctuation("$A、B$")


def test_internal_statement_name_is_detected():
    assert r2._contains_internal_fallback("ScalarGreaterEqualStatement")
    assert r2._contains_internal_fallback("TodaFooStatement")
    assert not r2._contains_internal_fallback("Toda Proposition 5.8 の結果")


def test_count_expectation_extracts_literal_and_count():
    assertion = _assert_node(
        'def test_x():\n    assert rendered.count("reason") == 2\n'
    )
    assert r2._count_expectation(assertion) == ("reason", 2, 2)


def test_r1_loader_reads_minimal_inventory(tmp_path: Path):
    csv_path = tmp_path / "inventory.csv"
    csv_path.write_text(
        "test_id,file,function,phase,primary_category\n"
        "tests/test_x.py::test_x,tests/test_x.py,test_x,154,current_contract\n",
        encoding="utf-8",
    )
    rows = r2._load_r1_rows(csv_path)
    assert rows["tests/test_x.py::test_x"].primary_category == "current_contract"


def test_reference_positive_expectation_is_recognized():
    assert r2._looks_like_reference_positive_expectation(
        "**[R1] Proposition 5.8.**"
    )
    assert not r2._looks_like_reference_positive_expectation(
        "Proposition 5.8 の結果"
    )


def test_phase_extraction_does_not_treat_core_as_old_phase():
    assert r2._phase_from_path(Path("test_phase154_example.py")) == "154"
    assert r2._phase_from_path(Path("test_proof.py")) == "core"

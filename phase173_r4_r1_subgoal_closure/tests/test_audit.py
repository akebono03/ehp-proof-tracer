"""Focused tests: source immutability, proof status and report integrity."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from phase173_r4_r1_subgoal_closure.audit import (
    classify_step,
    describe_progress,
    validate_lemma_source,
)


def lemma_fixture() -> str:
    return (
        "prefix\n"
        "\\begin{lemma}[]\n\\label{lem:5.4}\n"
        "\\nu_{4}\\in \\pi^{4}_{7}\n"
        "H(\\nu_{4})=\\iota_7,\\qquad 2E \\nu_{4}=E^{2}\\nu' .\n"
        "\\end{lemma}\n"
    )


def test_accepts_verified_lemma_environment() -> None:
    validate_lemma_source(lemma_fixture())


@pytest.mark.parametrize("needle", [
    "\\label{lem:5.4}",
    "\\nu_{4}\\in \\pi^{4}_{7}",
    "H(\\nu_{4})=\\iota_7",
    "2E \\nu_{4}=E^{2}\\nu'",
])
def test_rejects_missing_lemma_clause(needle: str) -> None:
    with pytest.raises(RuntimeError):
        validate_lemma_source(lemma_fixture().replace(needle, "MISSING"))


def test_rejects_duplicate_lemma() -> None:
    with pytest.raises(RuntimeError):
        validate_lemma_source(lemma_fixture() + lemma_fixture())


def test_proof_classification_correct_inference() -> None:
    expected = object()
    step = SimpleNamespace(conclusion=expected, rule=SimpleNamespace(value="inference"))
    assert classify_step(step, expected, required_rule="inference") == "PROVED:inference"


def test_rejects_given_instead_of_inference() -> None:
    expected = object()
    step = SimpleNamespace(conclusion=expected, rule=SimpleNamespace(value="given"))
    assert classify_step(step, expected, required_rule="inference") == "WRONG_RULE:given"


def test_rejects_other_conclusion() -> None:
    step = SimpleNamespace(conclusion=object(), rule=SimpleNamespace(value="inference"))
    assert classify_step(step, object()) == "WRONG_CONCLUSION"


def test_progress_reports_unresolved_and_proved() -> None:
    value = describe_progress([
        ("proved", "p"), ("unresolved", "a"), ("unresolved", "b"),
    ])
    assert value["proved_count"] == 1
    assert value["first_unresolved"] == ["a", "b"]
    assert value["last_unresolved"] == ["a", "b"]


def test_no_production_import_at_module_level() -> None:
    source = Path(__file__).resolve().parents[1].joinpath("audit.py").read_text(encoding="utf-8")
    before = source.split("def inspect_runtime(", 1)[0]
    assert "from phase165_" not in before
    assert "from phase173_r4_r1_source_bound_56" not in before

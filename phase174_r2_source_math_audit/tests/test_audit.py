"""Focused tests of Phase 174 R2 source extraction and audit contracts."""
from pathlib import Path

import pytest

from phase174_r2_source_math_audit.audit import (
    SOURCE_SPECS,
    TARGETS,
    extract_labeled_environment,
    source_evidence,
)


def test_source_specs_are_exact_and_reviewed() -> None:
    assert TARGETS == ((5, 3), (4, 8), (4, 9))
    assert tuple(item[1] for item in SOURCE_SPECS) == (
        "4.8", "lem:5.4", "eq:5.5", "eq:5.6", "prop:5.6",
    )


def test_source_extraction_uses_complete_labeled_environment() -> None:
    snippet = (
        "\\begin{equation}\\label{eq:5.5}\n"
        "2\\nu_n=E^n\\nu'\n"
        "\\end{equation}\n"
    )
    assert extract_labeled_environment(
        snippet, "eq:5.5", r"\begin{equation}", r"\end{equation}"
    ) == snippet.strip()


def test_source_extraction_rejects_duplicate_label() -> None:
    snippet = (
        r"\begin{equation}\label{eq:5.5}a\end{equation}" + "\n"
        + r"\begin{equation}\label{eq:5.5}b\end{equation}"
    )
    with pytest.raises(ValueError, match="ambiguous"):
        extract_labeled_environment(
            snippet, "eq:5.5", r"\begin{equation}", r"\end{equation}"
        )


def test_real_toda_sources_preserve_conditional_premise() -> None:
    root = Path(__file__).resolve().parents[2]
    evidence = source_evidence(root)
    assert len(evidence["mathematical_obligations"]) == 5
    assert all(
        item["verified_by_this_audit"] is False
        for item in evidence["mathematical_obligations"]
    )
    branch = evidence["source_segments"]["4.8"]
    assert r"\Delta(\iota_{2n-1})=0" in branch
    assert r"\mathbb{Z}_2" in branch
    assert r"2\nu_n=E^{\,n-3}\nu'" in evidence["source_segments"]["eq:5.5"]


def test_proposition_56_is_not_promoted_to_given() -> None:
    root = Path(__file__).resolve().parents[2]
    evidence = source_evidence(root)
    assert "nu5_double" in {
        item["name"] for item in evidence["mathematical_obligations"]
    }
    assert all(
        item["verified_by_this_audit"] is False
        for item in evidence["mathematical_obligations"]
    )

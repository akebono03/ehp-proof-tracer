"""R3K: conservative mathematical prose projection and frozen 1-stem regression."""
from __future__ import annotations

import re

import pytest

from proof import ProofRule, ProofStep
from phase169_r3k_narrative_projection import project_proven_map_property
from phase169_r3j_narrative_boundary_audit.audit import (
    build_audit, capture_actual_narrative, split_narrative,
)


@pytest.mark.parametrize("suffix, expected", (
    (r"\text{ is surjective}", "全射"),
    (r"\text{ is injective}", "単射"),
    (r"\text{ is the zero map}", "零写像"),
    (r"\text{ is an isomorphism}", "同型"),
))
def test_r3k_properties_preserve_exact_map_latex(suffix, expected):
    step = ProofStep(conclusion=object(), premises=(), rule=ProofRule.INFERENCE)
    latex = r"H: \pi_{6}^{3} \to \pi_{6}^{5}" + suffix
    assert project_proven_map_property(step, latex) == (
        r"$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は" + expected + "."
    )


def test_r3k_refuses_to_promote_given_or_unknown_words():
    given = ProofStep(conclusion=object(), premises=(), rule=ProofRule.GIVEN)
    inferred = ProofStep(conclusion=object(), premises=(), rule=ProofRule.INFERENCE)
    assert project_proven_map_property(given, r"E \text{ is surjective}") is None
    assert project_proven_map_property(inferred, r"E \text{ might be surjective}") is None


@pytest.fixture(scope="module")
def actual():
    return capture_actual_narrative()


def test_r3k_pi53_english_repetitions_and_citations(actual):
    result, model, markdown, view = actual
    report = build_audit(result, model, markdown, view)
    assert report["status"] == "complete"
    assert report["all_citations_mentioned"]
    assert not report["english_map_property_lines"]
    assert report["presentation_diagnostics"]["pi4_2_presentation_mentions"] == 1
    assert report["presentation_diagnostics"]["terminal_hopf_surjectivity_proven"]
    assert report["presentation_diagnostics"]["terminal_delta_injectivity_proven"]
    assert markdown.rstrip().endswith("□")
    assert any("全射" in line for line in markdown.splitlines())
    assert any("単射" in line for line in markdown.splitlines())
    assert "[R2]" in split_narrative(markdown)[1]

"""Application-level counterfeits are probes, not accepted mathematical facts."""
from __future__ import annotations

import pytest

from phase168_r3_41p8_trust_boundary_audit.audit import (
    ehp_counterfeit_probe, public_case_audit, stable_eta_counterfeit_probe,
)


@pytest.fixture(scope="module")
def public_cases():
    return public_case_audit()


def test_counterfeit_eta_is_rejected_by_actual_projection():
    result = stable_eta_counterfeit_probe()
    assert result["model_accepts_counterfeit_step"]
    assert result["same_typed_group_and_order"]
    assert result["counterfeit_has_definition_citation"]
    assert not result["unverified_rule_guard_accepts_counterfeit"]
    assert result["current_projection_rejects_counterfeit"]
    assert result["forced_bypass_would_emit_false_equation"]


def test_counterfeit_ehp_is_rejected_by_actual_projection(public_cases):
    _, valid_sample = public_cases
    result = ehp_counterfeit_probe(valid_sample)
    assert result["model_accepts_counterfeit_step"]
    assert result["exactness_premise_window_matches_conclusion"]
    assert result["original_indices_are_invalid"]
    assert not result["unverified_rule_guard_accepts_counterfeit"]
    assert result["current_projection_rejects_counterfeit"]
    assert result["forced_bypass_would_emit_false_exactness"]


@pytest.mark.parametrize("name", ("pi3_2", "pi4_3", "pi5_4"))
def test_public_fulltexts_and_citations_unchanged(name, public_cases):
    cases, _ = public_cases
    result = cases[name]
    assert result["fulltext_identical"]
    assert result["citation_integrity"]
    assert result["benchmark_pass"]
    assert result["expected_counts"]

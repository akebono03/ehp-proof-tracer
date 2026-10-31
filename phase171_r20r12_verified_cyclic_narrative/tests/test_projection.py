"""Proof-backed generator-order prose; forged or absent steps fail closed."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r20r12_verified_cyclic_narrative.projection import (
    suppress_exact_duplicate_body_lines, verified_order_four_summary,
)
from proof import ProofRule


@pytest.fixture(scope="module")
def prior_proof_model():
    root, ancestors, report = build_cyclic_pi63_proof()
    assert report["pi63_cyclic_group_proven"] is True
    return SimpleNamespace(
        steps=ancestors,
        root_index=next(i for i, step in enumerate(ancestors) if step is root),
    )


def test_real_prior_inferred_proof_has_cardinality_and_nonzero_double(prior_proof_model):
    paragraph = verified_order_four_summary(prior_proof_model)
    assert paragraph is not None
    assert r"\operatorname{ord}" in paragraph
    assert r"\neq0" in paragraph
    assert r"\cdot" in paragraph
    assert r"\longrightarrow" in paragraph
    assert "短完全列" in paragraph


def test_non_inferred_root_or_missing_ancestors_cannot_produce_prose(prior_proof_model):
    root = prior_proof_model.steps[prior_proof_model.root_index]
    forged = SimpleNamespace(conclusion=root.conclusion, rule=ProofRule.GIVEN, premises=())
    assert verified_order_four_summary(SimpleNamespace(steps=(forged,), root_index=0)) is None
    assert verified_order_four_summary(SimpleNamespace(steps=(root,), root_index=0)) is None
    assert verified_order_four_summary(SimpleNamespace(steps=(), root_index=None)) is None


def test_exact_duplicate_body_suppression_preserves_references_and_distinct_sources():
    rows = [
        "使用する結果", "", "[R1] source", "", "証明", "",
        "[R1]より, $E(\\eta_2)=\\eta_3$.", "",
        "[R1]より, $E(\\eta_2)=\\eta_3$.", "",
        "[R2]より, $E(\\eta_2)=\\eta_3$.", "",
        "以上より, $\\pi_6^3=\\mathbb{Z}/4$.",
    ]
    cleaned = suppress_exact_duplicate_body_lines(rows)
    assert cleaned.count("[R1]より, $E(\\eta_2)=\\eta_3$.") == 1
    assert "[R2]より, $E(\\eta_2)=\\eta_3$." in cleaned
    assert cleaned[2] == "[R1] source"
    assert cleaned[-1].startswith("以上より")


def test_duplicate_projection_rejects_invalid_input():
    with pytest.raises(TypeError):
        suppress_exact_duplicate_body_lines(["ok", None])

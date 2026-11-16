"""General-source manifest and citation boundary tests; no proof fabrication."""
from __future__ import annotations

import json

import pytest

from phase175_r3r6_lemma57_general import source


def reviewed_manifest() -> dict:
    return {
        "mode": "ORDERED_SOURCE_ONLY_MANIFEST",
        "assertions": [
            {
                "reference_id": "toda:Lemma 5.7",
                "statement_id": source.SOURCE_ID,
                "source_sha256": source.SOURCE_SHA256,
                "publication_position": 9100,
                "review_needed": False,
                "source_text": (
                    r"\alpha\in\pi_i(S^3) "
                    r"E^2\alpha\in2\iota_5\circ\pi_{i+2}(S^5) "
                    r"E(\eta_2\circ\alpha)=0"
                ),
            },
            {
                "reference_id": "toda:Proposition 5.8",
                "publication_position": 9200,
                "review_needed": False,
                "source_text": r"\begin{proposition}\label{prop:5.8}",
            },
        ],
    }


def test_manifest_requires_exact_prior_general_criterion(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(source, "verify_reviewed_toda_source", lambda root: {"source_blob": "verified"})
    path = tmp_path / source.MANIFEST
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(reviewed_manifest()), encoding="utf-8")
    result = source.verify_lemma57_manifest(tmp_path)
    assert result["lemma_position"] == 9100
    assert result["proposition_position"] == 9200
    assert result["new_concrete_given"] == 0


@pytest.mark.parametrize("mutation", ["missing", "wrong_hash", "wrong_order", "wrong_clause", "needs_review"])
def test_manifest_rejects_unreviewed_or_target_shadowing(monkeypatch, tmp_path, mutation: str) -> None:
    monkeypatch.setattr(source, "verify_reviewed_toda_source", lambda root: {"source_blob": "verified"})
    value = reviewed_manifest()
    lemma = value["assertions"][0]
    if mutation == "missing":
        value["assertions"].pop(0)
    elif mutation == "wrong_hash":
        lemma["source_sha256"] = "f" * 64
    elif mutation == "wrong_order":
        lemma["publication_position"] = 9300
    elif mutation == "wrong_clause":
        lemma["source_text"] = "not a general conditional"
    elif mutation == "needs_review":
        lemma["review_needed"] = True
    path = tmp_path / source.MANIFEST
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ValueError):
        source.verify_lemma57_manifest(tmp_path)


def test_general_source_type_is_not_a_particular_generator_image() -> None:
    general = source.TodaLemma57GeneralCriterion()
    assert general.domain_sphere == 3
    assert general.twice_suspended_sphere == 5
    assert not hasattr(general, "alpha")
    assert not hasattr(general, "target_generator")

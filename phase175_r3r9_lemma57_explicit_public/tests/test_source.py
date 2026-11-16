"""Source pinning and explicit-clause provenance tests."""
from __future__ import annotations

import json

import pytest

from phase175_r3r9_lemma57_explicit_public import source
from proof import ProofRule
from unified_statement_registry import AssertionOrigin


def manuscript(clause: str = source.PARTICULAR_CLAUSE) -> dict:
    """Only mock the immutable manifest shape, not the actual production source."""
    return {
        "assertions": [
            {
                "reference_id": "toda:Lemma 5.7",
                "statement_id": source.SOURCE_ID,
                "source_sha256": source.SOURCE_SHA256,
                "publication_position": source.SOURCE_POSITION,
                "review_needed": False,
                "source_text": (
                    r"\alpha\in\pi_i(S^3) "
                    r"E^2\alpha\in2\iota_5\circ\pi_{i+2}(S^5) "
                    r"E(\eta_2\circ\alpha)=0 特に, "
                    + clause + " "
                    + r"\Delta(\nu_5)=\pm(\eta_2\circ\nu')"
                ),
            },
        ],
    }


def write_manifest(root, record):
    location = root / source.MANIFEST
    location.parent.mkdir(parents=True, exist_ok=True)
    location.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")


def test_exact_explicit_source_and_order(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(source, "verify_lemma57_manifest", lambda root: {"original_pin": "verified"})
    write_manifest(tmp_path, manuscript())
    verified = source.verify_explicit_lemma57_source(tmp_path)
    assert verified["particular_clause"] == source.PARTICULAR_CLAUSE
    assert verified["new_group_given"] == 0
    assert verified["publication_position"] == 9100


@pytest.mark.parametrize("mutation", [
    "missing", "twice", "wrong_sha", "wrong_order", "needs_review", "without_specific",
])
def test_missing_or_changed_specific_clause_rejected(monkeypatch, tmp_path, mutation) -> None:
    monkeypatch.setattr(source, "verify_lemma57_manifest", lambda root: {"verified": True})
    row = manuscript()
    original = row["assertions"][0]
    if mutation == "missing":
        row["assertions"] = []
    elif mutation == "twice":
        original["source_text"] += " " + source.PARTICULAR_CLAUSE
    elif mutation == "wrong_sha":
        original["source_sha256"] = "0" * 64
    elif mutation == "wrong_order":
        original["publication_position"] = 9500
    elif mutation == "needs_review":
        original["review_needed"] = True
    elif mutation == "without_specific":
        original["source_text"] = original["source_text"].replace(
            source.PARTICULAR_CLAUSE, "E(eta_2 something)=0",
        )
    write_manifest(tmp_path, row)
    with pytest.raises(ValueError, match="R3R9_LEMMA57"):
        source.verify_explicit_lemma57_source(tmp_path)


def test_source_is_not_given_generator_image_or_group(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(source, "verify_explicit_lemma57_source", lambda root: {"verified": True})
    bridge = source.build_explicit_lemma57_source(tmp_path)
    assert len(bridge.proof_links) == 1
    link = bridge.proof_links[0]
    assert link.assertion_id == source.ASSERTION_ID
    assert link.step.rule is ProofRule.GIVEN
    assert link.step.conclusion == source.TodaLemma57ExplicitNuPrimeZero()
    assertion = bridge.registry.assertion(source.ASSERTION_ID)
    assert assertion.origin is AssertionOrigin.FIXED_STATEMENT
    assert bridge.registry.reference(source.REFERENCE_ID).publication_position == 9100
    assert type(link.step.conclusion).__name__ != "GeneratorImage"
    assert type(link.step.conclusion).__name__ != "Relation"

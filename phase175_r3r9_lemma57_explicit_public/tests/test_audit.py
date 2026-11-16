"""Ensure a claimed completion without the specific cited inference fails closed."""
from __future__ import annotations

from copy import deepcopy

import pytest

from phase175_r3r9_lemma57_explicit_public.audit import verify_public_result
from phase175_r3r9_lemma57_explicit_public.rule import RULE_NAME


def successful_minimum():
    return {
        "audit_result": "COMPLETE_AND_WEB_VERIFIED",
        "search_status": "complete",
        "search_open_count": 0,
        "search_conclusion_matches_db": True,
        "trust_verified": True,
        "model_root_verified": True,
        "web_key": "generic-complete-proof",
        "web_partial": False,
        "proof_steps": [
            {"rule": "GIVEN", "inference_rule": "Cited explicit nu-prime clause of Toda Lemma 5.7",
             "conclusion": "TodaLemma57ExplicitNuPrimeZero()", "premise_count": 0},
            {"rule": "INFERENCE", "inference_rule": RULE_NAME,
             "conclusion": "GeneratorImage(map=E, target=Zero())", "premise_count": 1},
        ],
        "references": [{"locator": "Lemma 5.7"}],
        "reference_count": 1,
    }


def test_direct_lemma57_gate_accepts_exact_provenance_shape() -> None:
    assert verify_public_result(successful_minimum())["lemma54_used"] is False


@pytest.mark.parametrize("mutation", ["not_complete", "given_image", "no_lemma57",
                                      "old_lemma54", "missing_extraction"])
def test_public_gate_fails_without_exact_cited_extraction(mutation: str) -> None:
    item = deepcopy(successful_minimum())
    if mutation == "not_complete":
        item["search_status"] = "partial"
    elif mutation == "given_image":
        item["proof_steps"][1]["rule"] = "GIVEN"
    elif mutation == "no_lemma57":
        item["references"] = []
    elif mutation == "old_lemma54":
        item["references"].append({"locator": "Lemma 5.4"})
    elif mutation == "missing_extraction":
        item["proof_steps"][1]["inference_rule"] = "another rule"
    with pytest.raises(RuntimeError, match="R3R9_PUBLIC_DIRECT_LEMMA57_NOT_VERIFIED"):
        verify_public_result(item)

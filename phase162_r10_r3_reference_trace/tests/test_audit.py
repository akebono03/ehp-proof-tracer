"""Lightweight read-only classifier contracts; no full-suite execution."""

from phase162_r10_r3_reference_trace.audit import classify


def test_cited_foundational_step_precedes_rule_type():
    node = {"foundational_key": "literature:(5.3):nu_prime_hopf_relation", "classification": None, "rule": "GIVEN"}
    assert classify(node) == "CITED_BOUNDARY"


def test_fixed_proof_and_internal_have_distinct_classes():
    assert classify({"classification": "fixed_statement", "rule": "INFERENCE"}) == "FIXED_STATEMENT"
    assert classify({"classification": "proof_internal", "rule": "INFERENCE"}) == "PROOF_INTERNAL"


def test_unclassified_inference_and_given_remain_distinct():
    assert classify({"classification": None, "rule": "INFERENCE"}) == "UNCLASSIFIED_INFERENCE"
    assert classify({"classification": None, "rule": "GIVEN"}) == "OTHER_GIVEN"

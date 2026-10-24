"""Package-local audit utilities; no repository imports are needed."""
from __future__ import annotations

from phase168_r3_41p8_trust_boundary_audit.audit import CASES, evaluate, hash_bytes, report_text


def test_fixed_cases_are_all_three_public_goals():
    assert {(n, k) for _, n, k, _, _ in CASES} == {(2, 1), (3, 1), (4, 1)}


def test_hash_bytes_is_deterministic():
    assert hash_bytes(b"proof") == hash_bytes(b"proof")
    assert hash_bytes(b"proof") != hash_bytes(b"not proof")


def test_missing_report_fails_closed():
    passed, checks = evaluate({"cases": {}, "counterfeit_probes": {}})
    assert not passed
    assert False in checks


def test_report_contains_boundary_outcome():
    report = {"cases": {}, "counterfeit_probes": {"stable_eta": {}, "ehp": {}}, "status": "PASS"}
    text = report_text(report)
    assert "trust boundary" in text
    assert "ProofNarrativeModel" in text
    assert "PASS" in text

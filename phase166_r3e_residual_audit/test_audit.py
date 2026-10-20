"""Focused, read-only Phase 166 R3-E audit integrity tests."""
from __future__ import annotations

from pathlib import Path

import audit


def test_runtime_report_covers_both_requested_groups():
    result = audit.run()
    assert [(x["n"], x["k"]) for x in result["cases"]] == [(3, 1), (4, 1)]
    assert all(x["status"] == "complete" and x["unique_root"] for x in result["cases"])


def test_pi43_rule_name_is_observable_without_modifying_renderer():
    case = audit.inspect_case(3, 1)
    assert "infinite cyclic quotient structure" in case["narrative"]
    assert case["raw_quotient_rule_in_markdown"]


def test_pi54_selected_path_is_cited_specialization():
    case = audit.inspect_case(4, 1)
    assert case["generic_eta_specialization_in_ancestry"]
    assert not case["has_transport_proof_ancestry"]
    assert "Proposition 5.1" in case["narrative"]


def test_audit_does_not_create_new_production_file():
    assert (Path(__file__).resolve().parent / "audit.py").is_file()
    assert audit.ROOT.is_dir()

"""Focused evidence-inventory tests, independent of the live repository."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit import interesting_evidence, scalar_evidence


def test_scalar_evidence_retains_actual_nested_paths():
    records = scalar_evidence({"nested": {"candidate_count": 0, "inferred": True}, "goals": ["x"]})
    assert {item["path"]: item["value"] for item in records} == {
        "nested.candidate_count": 0, "nested.inferred": True, "goals[0]": "x",
    }


def test_interesting_evidence_does_not_fabricate_zero_status():
    records = scalar_evidence({"other": "data", "proof": {"status": "search_failed"}})
    assert interesting_evidence(records) == [{"path": "proof.status", "value": "search_failed"}]


def test_scalar_evidence_caps_long_strings():
    value = scalar_evidence({"source": "a" * 400})[0]["value"]
    assert len(value) < 400
    assert value.endswith("[truncated]")


def test_scalar_evidence_handles_empty_and_null():
    assert scalar_evidence({"empty": [], "null": None}) == [{"path": "null", "value": None}]

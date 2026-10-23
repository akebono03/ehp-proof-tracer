"""Narrow report-shape validation. Runtime proof search is executed by audit.py."""
import json
from pathlib import Path

REPORT = Path(__file__).resolve().parents[1] / "output" / "audit.json"


def test_report_is_runtime_observation():
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    assert data["mode"] == "AUDIT_ONLY"
    assert data["group"] == "pi_5^4"
    assert data["step_count"] == len(data["steps"])


def test_reference_links_have_consistent_step_numbers():
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    for citation in data["citations"]:
        number = citation["number"]
        for i in citation["step_indices"]:
            assert number in data["steps"][i]["citation_numbers"]
        assert citation["inference_only"] == (not citation["assertion_ids"])

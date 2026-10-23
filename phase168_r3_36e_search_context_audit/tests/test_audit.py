"""Report validation only, not whole-repository tests."""
import json
from pathlib import Path

REPORT = Path(__file__).resolve().parents[1] / "output" / "audit.json"


def test_actual_search_context_captured():
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    assert data["mode"] == "AUDIT_ONLY"
    assert data["goal"] == "pi_5^4"
    assert data["context_captured_count"] == 1


def test_model_citations_retain_used_step_indices():
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    for citation in data["search_context_citations"]:
        assert citation["step_indices"]
        assert citation["number"] > 0

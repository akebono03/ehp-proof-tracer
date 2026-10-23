"""R3-36C isolated report validation."""
import json
from pathlib import Path

REPORT = Path(__file__).resolve().parents[1] / "output" / "audit.json"


def test_given_step_report_shape():
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    assert data["mode"] == "AUDIT_ONLY"
    assert data["target"] == "pi_5^4"
    assert isinstance(data["given_steps"], list)


def test_exact_link_is_consistent():
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    for step in data["given_steps"]:
        assert isinstance(step["registered_exact_content"], list)
        for link in step["links_same_step_or_conclusion"]:
            assert link["kind"] in ("exact", "same_conclusion")
            assert link["link_matches_conclusion"]

import json
from pathlib import Path

REPORT = Path(__file__).resolve().parents[1] / "output" / "audit.json"


def test_three_cases_and_reference_contents():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert [item["target"] for item in report["cases"]] == [
        "pi_3^2", "pi_4^3", "pi_5^4",
    ]
    assert all(item["references"] for item in report["cases"])
    assert all(ref["contents"] for item in report["cases"]
               for ref in item["references"])


def test_pi54_toda_specialization_is_present_in_proof_steps():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    pi54 = report["cases"][2]
    matches = [
        step for step in pi54["steps"]
        if step["kind"] == "Toda45IsomorphismStatement"
    ]
    assert len(matches) >= 2

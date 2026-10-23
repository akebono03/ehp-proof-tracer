"""Limited R3-37 output integrity tests; no full-suite execution."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "output"


def test_three_public_model_outputs_saved():
    report = json.loads((OUT / "audit.json").read_text(encoding="utf-8"))
    assert report["mode"] == "AUDIT_ONLY"
    assert {x["target"] for x in report["cases"]} == {
        "pi_3^2", "pi_4^3", "pi_5^4",
    }
    assert all(x["model_render_calls"] == 1 for x in report["cases"])


def test_public_reference_headings_match_model_numbers():
    report = json.loads((OUT / "audit.json").read_text(encoding="utf-8"))
    for case in report["cases"]:
        assert "使用する結果" in case["reference_section"]
        assert case["proof_section"].strip()
        for item in case["references"]:
            assert f'**[R{item["number"]}] {item["locator"]}.**' in case["reference_section"]

import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "output"


def test_all_three_frozen_originals_compared():
    d=json.loads((OUT/"audit.json").read_text(encoding="utf-8"))
    assert d["mode"] == "AUDIT_ONLY"
    assert [c["name"] for c in d["cases"]] == ["pi3_2","pi4_3","pi5_4"]
    for case in d["cases"]:
        for section in ("reference","proof"):
            assert (OUT/case["comparison"][section]["diff_file"]).is_file()
        assert len(case["baseline_sha256"]) == 64


def test_reference_model_bodies_reported():
    d=json.loads((OUT/"audit.json").read_text(encoding="utf-8"))
    for case in d["cases"]:
        assert case["reference_entries"]
        assert all(item["assertion_ids"] for item in case["reference_entries"])
        assert all(isinstance(item["body_count"],int) for item in case["reference_entries"])

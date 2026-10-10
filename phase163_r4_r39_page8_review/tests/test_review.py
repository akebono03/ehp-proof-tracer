import csv
import json
from pathlib import Path
import pytest
from phase163_r4_r39_page8_review.review import (
    ANCHORS, EVIDENCE, EXPECTED_SHA256, review_page_eight, run, sha256, validate_inputs
)
BASE = Path(__file__).resolve().parent.parent

def baseline():
    return (BASE / "R38_BASELINE.tex").read_text(encoding="utf-8")

def ledger():
    return json.loads((BASE / "R38_PAGE_LEDGER.json").read_text(encoding="utf-8"))

def test_baseline_sha():
    assert sha256(baseline()) == EXPECTED_SHA256

def test_source_anchors():
    assert len(ANCHORS) == 10
    validate_inputs(baseline(), ledger())

def test_full_ledger_preserved():
    result = review_page_eight(baseline(), ledger())
    assert len(result) == 11
    assert [r["printed_page"] for r in result] == list(range(5,16))

def test_statuses_remain_conservative():
    result = review_page_eight(baseline(), ledger())
    assert [r["status"] for r in result] == ["VERIFIED"] * 3 + ["UNVERIFIED"] * 8

def test_review_ledger_not_mutated():
    old = ledger()
    review_page_eight(baseline(), old)
    assert old[3].get("unresolved_review_topics") is None

def test_source_mismatch_rejected():
    with pytest.raises(ValueError, match="SHA-256"):
        validate_inputs(baseline()+" ", ledger())

def test_wrong_status_rejected():
    old = ledger()
    old[3]["status"] = "VERIFIED"
    with pytest.raises(ValueError, match="verification states"):
        validate_inputs(baseline(), old)

def test_review_evidence_retained():
    assert len(EVIDENCE) == 10
    assert sum(x[2] == "REQUIRES_CONTEXT_REVIEW" for x in EVIDENCE) == 2

def test_run_writes_utf8_outputs(tmp_path):
    src=tmp_path/"source.tex"
    src.write_text(baseline(),encoding="utf-8")
    led=tmp_path/"ledger.json"
    led.write_text(json.dumps(ledger(),ensure_ascii=False),encoding="utf-8")
    s=run(src,led,tmp_path/"out")
    assert s["status_counts"] == {"VERIFIED":3,"UNVERIFIED":8,"CORRECTION_REQUIRED":0}
    assert s["total_recorded_corrections"] == 18
    assert (tmp_path/"out"/"Toda_01_corrected.tex").read_text(encoding="utf-8") == baseline()
    with (tmp_path/"out"/"page8_evidence.csv").open(encoding="utf-8-sig",newline="") as f:
        assert len(list(csv.DictReader(f))) == 10

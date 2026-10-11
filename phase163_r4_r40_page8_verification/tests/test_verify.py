import csv
import json
from pathlib import Path

import pytest

from phase163_r4_r40_page8_verification.verify import (
    ANCHORS, EVIDENCE, EXPECTED_SHA256, run, sha256,
    validate_inputs, verify_page_eight,
)

BASE = Path(__file__).resolve().parent.parent


def baseline():
    return (BASE / "R39_BASELINE.tex").read_text(encoding="utf-8")


def ledger():
    return json.loads((BASE / "R39_PAGE_LEDGER.json").read_text(encoding="utf-8"))


def test_baseline_sha():
    assert sha256(baseline()) == EXPECTED_SHA256


def test_anchors():
    assert len(ANCHORS) == 13
    validate_inputs(baseline(), ledger())


def test_page_eight_becomes_verified():
    new = verify_page_eight(baseline(), ledger())
    assert [row["status"] for row in new] == ["VERIFIED"] * 4 + ["UNVERIFIED"] * 7


def test_provenance_caveat_preserved():
    page = verify_page_eight(baseline(), ledger())[3]
    assert page["verbatim_transcription_verified"] is False
    assert page["source_claim_independently_proven"] is False


def test_original_ledger_unchanged():
    old = ledger()
    verify_page_eight(baseline(), old)
    assert old[3]["status"] == "UNVERIFIED"


def test_wrong_source_rejected():
    with pytest.raises(ValueError, match="SHA-256"):
        validate_inputs(baseline() + " ", ledger())


def test_wrong_status_rejected():
    old = ledger()
    old[3]["status"] = "VERIFIED"
    with pytest.raises(ValueError, match="preceding status"):
        validate_inputs(baseline(), old)


def test_evidence_and_boundary():
    assert len(EVIDENCE) == 10
    assert sum("CAVEAT" in row[2] or "BOUNDARY" in row[2] for row in EVIDENCE) == 2


def test_run_outputs(tmp_path):
    source = tmp_path / "source.tex"
    source.write_text(baseline(), encoding="utf-8")
    ledger_path = tmp_path / "ledger.json"
    ledger_path.write_text(json.dumps(ledger(), ensure_ascii=False), encoding="utf-8")
    result = run(source, ledger_path, tmp_path / "out")
    assert result["status_counts"] == {"VERIFIED": 4, "UNVERIFIED": 7, "CORRECTION_REQUIRED": 0}
    assert result["total_recorded_corrections"] == 18
    assert (tmp_path / "out" / "Toda_01_corrected.tex").read_text(encoding="utf-8") == baseline()
    with (tmp_path / "out" / "page8_evidence.csv").open(encoding="utf-8-sig", newline="") as handle:
        assert len(list(csv.DictReader(handle))) == 10

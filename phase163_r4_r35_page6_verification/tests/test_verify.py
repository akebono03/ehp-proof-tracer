import json
from pathlib import Path

import pytest

from phase163_r4_r35_page6_verification.verify import (
    EXPECTED_SHA256, REQUIRED, run, sha256, validate_inputs, verify_page_six,
)

HERE = Path(__file__).resolve().parents[1]


def baseline():
    return (HERE / "R34_BASELINE.tex").read_text(encoding="utf-8")


def ledger():
    return json.loads((HERE / "R34_PAGE_LEDGER.json").read_text(encoding="utf-8"))


def test_baseline_sha256():
    assert sha256(baseline()) == EXPECTED_SHA256


def test_required_mathematical_passages_are_present():
    assert all(fragment in baseline() for fragment in REQUIRED)


def test_validation_accepts_expected_inputs():
    validate_inputs(baseline(), ledger())


def test_source_guard_rejects_other_tex():
    with pytest.raises(ValueError, match="SHA-256"):
        validate_inputs(baseline() + "x", ledger())


def test_rejects_preverified_page_six():
    original = ledger()
    original[1]["status"] = "VERIFIED"
    with pytest.raises(ValueError, match="statuses"):
        verify_page_six(baseline(), original)


def test_rejects_short_ledger():
    with pytest.raises(ValueError, match="eleven"):
        validate_inputs(baseline(), ledger()[:-1])


def test_verifies_only_page_six():
    updated = verify_page_six(baseline(), ledger())
    assert [x["status"] for x in updated] == ["VERIFIED", "VERIFIED"] + ["UNVERIFIED"] * 9
    assert updated[1]["verbatim_transcription_verified"] is False
    assert updated[2:] == ledger()[2:]


def test_no_tex_mutation(tmp_path):
    source = HERE / "R34_BASELINE.tex"
    summary = run(source, HERE / "R34_PAGE_LEDGER.json", tmp_path)
    assert summary["input_sha256"] == summary["output_sha256"]
    assert (tmp_path / "Toda_01_corrected.tex").read_text(encoding="utf-8") == baseline()


def test_complete_outputs(tmp_path):
    summary = run(HERE / "R34_BASELINE.tex", HERE / "R34_PAGE_LEDGER.json", tmp_path)
    assert summary["total_recorded_corrections"] == 18
    assert summary["status_counts"] == {"VERIFIED": 2, "UNVERIFIED": 9, "CORRECTION_REQUIRED": 0}
    for name in ("page_ledger.json", "page_ledger.csv", "page6_evidence.csv", "summary.json", "report.md"):
        assert (tmp_path / name).exists()

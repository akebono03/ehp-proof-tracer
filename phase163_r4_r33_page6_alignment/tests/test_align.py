import json
from pathlib import Path

import pytest

from phase163_r4_r33_page6_alignment.align import (
    AFTER,
    BEFORE,
    EXPECTED_SHA256,
    correct,
    run,
    sha256,
    update_ledger,
)

HERE = Path(__file__).resolve().parents[1]


def baseline():
    return (HERE / "R32_BASELINE.tex").read_text(encoding="utf-8")


def ledger():
    return json.loads((HERE / "R32_PAGE_LEDGER.json").read_text(encoding="utf-8"))


def test_baseline_sha256():
    assert sha256(baseline()) == EXPECTED_SHA256


def test_basepoint_conditions_have_unique_location():
    assert baseline().count(BEFORE) == 1


def test_explicit_conditions_restored():
    revised = correct(baseline())
    assert AFTER in revised
    assert "$f(a_0)=a'_0$" in revised
    assert "$g(b_0)=b'_0$" in revised


def test_preserves_previous_sphere_equations():
    revised = correct(baseline())
    assert r"\shrink_{m,n}:S^m\times S^n\longrightarrow S^{m+n}" in revised
    assert r"\shrink_{m+n,p}" in revised


def test_wrong_input_sha_fails():
    with pytest.raises(ValueError, match="SHA-256"):
        correct(baseline() + "changed")


def test_page_ledger_has_one_verified_page():
    revised = update_ledger(ledger(), "new-sha")
    assert [x["status"] for x in revised] == ["VERIFIED"] + ["UNVERIFIED"] * 10
    assert all(x["source_sha256"] == "new-sha" for x in revised)


def test_ledger_wrong_state_fails():
    data = ledger()
    data[1]["status"] = "VERIFIED"
    with pytest.raises(ValueError, match="statuses"):
        update_ledger(data, "new-sha")


def test_run_writes_full_utf8_files(tmp_path):
    result = run(HERE / "R32_BASELINE.tex", HERE / "R32_PAGE_LEDGER.json", tmp_path)
    assert result["total_recorded_corrections"] == 17
    assert result["status_counts"] == {"VERIFIED": 1, "UNVERIFIED": 10, "CORRECTION_REQUIRED": 0}
    assert (tmp_path / "Toda_01_corrected.tex").read_text(encoding="utf-8") == correct(baseline())
    assert (tmp_path / "alignment_review.csv").exists()
    assert (tmp_path / "report.md").exists()

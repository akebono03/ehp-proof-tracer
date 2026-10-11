import json
from pathlib import Path

import pytest

from phase163_r4_r34_page6_alignment.align import (
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
    return (HERE / "R33_BASELINE.tex").read_text(encoding="utf-8")


def ledger():
    return json.loads((HERE / "R33_PAGE_LEDGER.json").read_text(encoding="utf-8"))


def test_baseline_hash():
    assert sha256(baseline()) == EXPECTED_SHA256


def test_unique_equation_location():
    assert baseline().count(BEFORE) == 1


def test_based_domains_and_codomain():
    result = correct(baseline())
    assert AFTER in result
    assert r"(A\wedge B,a_0\wedge b_0)" in result
    assert r"(B,b_0)\to(B',b'_0)" in result


def test_previous_corrections_preserved():
    result = correct(baseline())
    assert r"\shrink_{m,n}:S^m\times S^n\longrightarrow S^{m+n}" in result
    assert r"f(a_0)=a'_0" in result
    assert r"g(b_0)=b'_0" in result


def test_source_guard():
    with pytest.raises(ValueError, match="SHA-256"):
        correct(baseline() + "changed")


def test_ledger_status_preserved():
    result = update_ledger(ledger(), "new-hash")
    assert [row["status"] for row in result] == ["VERIFIED"] + ["UNVERIFIED"] * 10
    assert all(row["source_sha256"] == "new-hash" for row in result)


def test_reject_incorrect_page_status():
    data = ledger()
    data[1]["status"] = "VERIFIED"
    with pytest.raises(ValueError, match="statuses"):
        update_ledger(data, "new-hash")


def test_reject_missing_page():
    with pytest.raises(ValueError, match="11"):
        update_ledger(ledger()[:-1], "new-hash")


def test_run_complete_utf8_outputs(tmp_path):
    result = run(HERE / "R33_BASELINE.tex", HERE / "R33_PAGE_LEDGER.json", tmp_path)
    assert result["total_recorded_corrections"] == 18
    assert result["status_counts"]["VERIFIED"] == 1
    assert (tmp_path / "Toda_01_corrected.tex").read_text(encoding="utf-8") == correct(baseline())
    assert (tmp_path / "alignment_review.csv").exists()
    assert (tmp_path / "page_ledger.json").exists()

import hashlib
from pathlib import Path

import pytest

from phase163_r4_r27_page_ledger.ledger import (
    CORRECTION_HISTORY,
    EXPECTED_R26_SHA256,
    REVIEW_FIELDS,
    build_summary,
    make_ledger,
    read_tex,
    run,
    validate_ledger,
    validate_source,
)


def test_all_eleven_pages_are_present_and_not_auto_verified():
    rows = make_ledger(EXPECTED_R26_SHA256)
    assert [(r["pdf_page"], r["printed_page"]) for r in rows] == [(i, i + 4) for i in range(1, 12)]
    assert all(r["status"] == "UNVERIFIED" for r in rows)
    assert all(not any(r["review"].values()) for r in rows)


def test_history_preserves_nine_prior_corrections_without_verifying_pages():
    rows = make_ledger(EXPECTED_R26_SHA256)
    assert sum(r["prior_corrections"] for r in rows) == 9
    assert sum(x[3] for x in CORRECTION_HISTORY) == 9
    assert build_summary(rows, EXPECTED_R26_SHA256)["chapter_fully_verified"] is False


def test_verified_requires_complete_review_and_specific_evidence():
    rows = make_ledger(EXPECTED_R26_SHA256)
    rows[0]["status"] = "VERIFIED"
    with pytest.raises(ValueError):
        validate_ledger(rows, EXPECTED_R26_SHA256)
    rows[0]["review"] = {key: True for key in REVIEW_FIELDS}
    with pytest.raises(ValueError):
        validate_ledger(rows, EXPECTED_R26_SHA256)
    rows[0]["reviewer"] = "reviewer"
    rows[0]["evidence_note"] = "PDF page 1 and corresponding TeX full-text checked"
    validate_ledger(rows, EXPECTED_R26_SHA256)


def test_missing_page_or_changed_tex_hash_fails():
    rows = make_ledger(EXPECTED_R26_SHA256)
    with pytest.raises(ValueError):
        validate_ledger(rows[:-1], EXPECTED_R26_SHA256)
    rows[3]["source_sha256"] = "wrong"
    with pytest.raises(ValueError):
        validate_ledger(rows, EXPECTED_R26_SHA256)


def test_r26_fixture_uses_expected_sha():
    fixture = Path(__file__).resolve().parents[1] / "R26_BASELINE.tex"
    content = read_tex(fixture)
    assert hashlib.sha256(content.encode("utf-8")).hexdigest() == EXPECTED_R26_SHA256
    assert validate_source(fixture)[1] == EXPECTED_R26_SHA256


def test_wrong_source_never_changes_output(tmp_path):
    src = tmp_path / "wrong.tex"
    src.write_text("incorrect file", encoding="utf-8")
    dest = tmp_path / "output"
    with pytest.raises(ValueError):
        run(src, dest)
    assert not dest.exists()


def test_report_generation_and_no_tex_rewrite(tmp_path):
    fixture = Path(__file__).resolve().parents[1] / "R26_BASELINE.tex"
    dest = tmp_path / "out"
    before = fixture.read_bytes()
    summary = run(fixture, dest)
    assert summary["status_counts"] == {"UNVERIFIED": 11, "CORRECTION_REQUIRED": 0, "VERIFIED": 0}
    assert summary["prior_confirmed_corrections"] == 9
    assert fixture.read_bytes() == before
    assert sorted(p.name for p in dest.iterdir()) == ["correction_history.csv", "page_ledger.csv", "page_ledger.json", "report.md", "summary.json"]


def test_full_completion_only_with_eleven_verified_pages():
    rows = make_ledger(EXPECTED_R26_SHA256)
    for row in rows:
        row["status"] = "VERIFIED"
        row["review"] = {key: True for key in REVIEW_FIELDS}
        row["reviewer"] = "checked"
        row["evidence_note"] = "All five categories checked against printed original"
    assert build_summary(rows, EXPECTED_R26_SHA256)["chapter_fully_verified"] is True

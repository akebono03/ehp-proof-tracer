"""R72 focused tests for prior evidence, document gaps, and fail-closed checks."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from phase174_r3_r7_r71_common_narrative_regression.audit import (
    PINS as R71_PINS,
    REVIEWED_REMOTE_HEAD,
)
from phase174_r3_r7_r72_closeout_preflight.audit import (
    ALLOWED_LOCAL_HEADS,
    MERGED_R71_HEAD,
    DOCUMENTS,
    EXPECTED_REFERENCES,
    INCOMPLETE_CASES,
    check_prior_package,
    document_readiness,
    git_blob_sha,
    validate_r71_report,
)


def fixture_prior() -> dict[str, object]:
    """Build a small simulated R71 report; no source search is bypassed."""
    return {
        "phase": "174-R71",
        "reviewed_remote_head": REVIEWED_REMOTE_HEAD,
        "local_head": REVIEWED_REMOTE_HEAD,
        "source_files_checked": list(R71_PINS),
        "production_changes": [],
        "new_given": 0,
        "new_mathematical_rules": 0,
        "whole_test_suite_executed": False,
        "full_sentence_semantics_certified": False,
        "public_samples": [
            {"n": n, "k": k, "group": f"pi_{n+k}^{n}",
             "status": "COMPLETE", "verified_root": True,
             "step_count": 5, "reference_count": refs,
             "markdown_sha256": "a" * 64}
            for (n, k), refs in EXPECTED_REFERENCES.items()
        ],
    }


def test_r71_evidence_accepts_exact_completed_case_contract() -> None:
    report = fixture_prior()
    result = validate_r71_report(report, REVIEWED_REMOTE_HEAD)
    assert len(result) == 8
    assert [item["reference_count"] for item in result] == list(EXPECTED_REFERENCES.values())


def test_r71_evidence_survives_audit_only_r71_merge() -> None:
    result = validate_r71_report(fixture_prior(), MERGED_R71_HEAD)
    assert len(result) == len(EXPECTED_REFERENCES)
    assert ALLOWED_LOCAL_HEADS == (REVIEWED_REMOTE_HEAD, MERGED_R71_HEAD)


def test_r71_evidence_rejects_duplicate_complete_case() -> None:
    report = fixture_prior()
    report["public_samples"][1] = deepcopy(report["public_samples"][0])
    with pytest.raises(RuntimeError, match="R72_R71_SAMPLE_UNEXPECTED_OR_DUPLICATED"):
        validate_r71_report(report, REVIEWED_REMOTE_HEAD)


def test_r71_evidence_rejects_promoted_or_unverified_case() -> None:
    report = fixture_prior()
    report["public_samples"][0]["verified_root"] = False
    with pytest.raises(RuntimeError, match="R72_R71_SAMPLE_CONTRACT_CHANGED"):
        validate_r71_report(report, REVIEWED_REMOTE_HEAD)


def test_r71_evidence_rejects_changed_reference_count() -> None:
    report = fixture_prior()
    report["public_samples"][0]["reference_count"] = 99
    with pytest.raises(RuntimeError, match="R72_R71_SAMPLE_CONTRACT_CHANGED"):
        validate_r71_report(report, REVIEWED_REMOTE_HEAD)


def test_r71_evidence_rejects_full_test_or_sentence_certification_claim() -> None:
    report = fixture_prior()
    report["whole_test_suite_executed"] = True
    with pytest.raises(RuntimeError, match="R72_R71_REPORT_SCOPE_CHANGED"):
        validate_r71_report(report, REVIEWED_REMOTE_HEAD)
    report = fixture_prior()
    report["full_sentence_semantics_certified"] = True
    with pytest.raises(RuntimeError, match="R72_R71_REPORT_SCOPE_CHANGED"):
        validate_r71_report(report, REVIEWED_REMOTE_HEAD)


def test_r71_evidence_rejects_different_head() -> None:
    with pytest.raises(RuntimeError, match="R72_HEAD_REVIEW_REQUIRED"):
        validate_r71_report(fixture_prior(), "a" * 40)


def test_prior_r71_report_head_cannot_be_rewritten_to_merge_head() -> None:
    report = fixture_prior()
    report["local_head"] = MERGED_R71_HEAD
    with pytest.raises(RuntimeError, match="R72_R71_REPORT_HEAD_MISMATCH"):
        validate_r71_report(report, MERGED_R71_HEAD)


def test_document_gap_detection_does_not_mutate_files(tmp_path: Path) -> None:
    original = {}
    for path in DOCUMENTS:
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        text = "# EHP Proof Tracer\n\n<!-- PHASE173_FINAL_CLOSEOUT_20261105 -->\n"
        target.write_text(text, encoding="utf-8")
        original[path] = target.read_bytes()
    report = document_readiness(tmp_path)
    assert len(report) == 5
    assert all(item["closeout_full_file_update_required"] for item in report)
    assert all((tmp_path / path).read_bytes() == raw for path, raw in original.items())


def test_document_gap_can_be_cleared_by_an_actual_closeout_marker(tmp_path: Path) -> None:
    for path in DOCUMENTS:
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            "# EHP Proof Tracer\n<!-- PHASE173_FINAL_CLOSEOUT_20261105 -->\n"
            "<!-- PHASE174_FINAL_CLOSEOUT_20261111 -->\n", encoding="utf-8",
        )
    assert all(not item["closeout_full_file_update_required"]
               for item in document_readiness(tmp_path))


def test_document_history_missing_fails_closed(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# EHP Proof Tracer\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="R72_PHASE173_HISTORY_MISSING"):
        document_readiness(tmp_path)


def test_r71_prior_audit_script_is_source_pinned() -> None:
    root = Path(__file__).resolve().parents[2]
    check_prior_package(root)


def test_git_blob_fingerprint_and_partial_sample_contract() -> None:
    assert git_blob_sha(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"
    assert INCOMPLETE_CASES == ((4, 8), (4, 31))

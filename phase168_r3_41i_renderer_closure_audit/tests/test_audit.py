"""Focused unit tests for read-only closure-audit interpretation."""
from pathlib import Path

from phase168_r3_41i_renderer_closure_audit.audit import (
    inspect_route_contract, render_report, summarize_comparison,
)


def _comparison():
    return {
        "name": "pi5_4", "baseline_path": "fixed/pi5_4_original.txt",
        "baseline_sha256": "a" * 64, "rendered_step_count": 10,
        "web_partial": False,
        "reference_entries": [
            {"number": 1, "locator": "(4.5)", "body_count": 1},
            {"number": 2, "locator": "Proposition 5.1", "body_count": 1},
        ],
        "comparison": {
            "reference": {"exact_after_line_cleanup": False, "difference_line_count": 9},
            "proof": {"exact_after_line_cleanup": False, "difference_line_count": 8},
        },
    }


def _text():
    return (
        "使用する結果\n\n**[R1] (4.5).**\n\n"
        "**[R2] Proposition 5.1.**\n\n証明\n\n"
        "[R1]を (n,m,k)=(3,4,1) に適用すると, "
        "$E:\\pi_{4}^{3}\\to\\pi_{5}^{4}$ は同型.\n"
        "$\\pi_{4}^{3}=\\mathbb{Z}/2\\{\\eta_{3}\\}$.\n"
        "$E(\\eta_{3})=\\eta_{4}$.\n□\n"
    )


def test_reference_heading_numbers_are_not_proof_line_numbers():
    row = summarize_comparison(_comparison(), _text())
    assert row["model_reference_numbers"] == [1, 2]
    assert row["used_reference_numbers_in_proof"] == [1]
    assert row["references_not_explicitly_tagged_in_proof"] == [2]
    assert "PROOF_HAS_DANGLING_REFERENCE_NUMBERS" not in row["issues"]


def test_frozen_text_differences_are_reported_for_manual_review():
    row = summarize_comparison(_comparison(), _text())
    assert row["reference_difference_lines"] == 9
    assert row["proof_difference_lines"] == 8
    assert "MANUAL_FROZEN_TEXT_REVIEW_REQUIRED" in row["issues"]
    assert "COMPLETE_MARKER_MISSING" not in row["issues"]


def test_missing_reference_body_is_distinct_from_explanation_gap():
    comparison = _comparison()
    comparison["reference_entries"][0]["body_count"] = 0
    row = summarize_comparison(comparison, _text())
    assert row["missing_body_locators"] == ["(4.5)"]
    assert "REFERENCE_BODIES_MISSING" in row["issues"]


def test_proof_citing_unknown_reference_is_reported():
    row = summarize_comparison(_comparison(), _text().replace("[R1]を", "[R7]を"))
    assert "PROOF_HAS_DANGLING_REFERENCE_NUMBERS" in row["issues"]


def test_report_does_not_claim_frozen_text_passes_when_differing():
    row = summarize_comparison(_comparison(), _text())
    report = render_report([row], {"model": True}, [])
    assert "MANUAL_FROZEN_TEXT_REVIEW_REQUIRED" in report
    assert "全文一致を意味しない" in report
    assert "pi5_4_frozen.txt" in report


def test_public_route_contract_uses_current_repository_files():
    root = Path(__file__).resolve().parents[2]
    report = inspect_route_contract(root)
    assert report["standard_model_is_default"]
    assert report["standard_explicit_legacy_retained"]
    assert report["adapter_legacy_fallback_retained"]
    assert report["partial_step_uses_model_citation_numbers"]

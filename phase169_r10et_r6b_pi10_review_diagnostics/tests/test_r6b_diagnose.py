"""Focused read-only diagnostic tests; no EHP application imports required."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase169_r10et_r6b_pi10_review_diagnostics.diagnose import (
    diagnostic_lines,
    existing_report,
)


def sample_report(problems: list[str]) -> dict:
    return {
        "phase": "169 R10ET-R6", "mode": "AUDIT_ONLY",
        "required_pass": True, "probes_pass": False,
        "cases": [{
            "case": "pi_10^8", "trust": "PASS", "status": "complete",
            "eligible_image_steps": 4, "canonical_image_steps": 3,
            "remaining_eligible_cited_steps": 0,
            "reference_locators": ["DB prior:", "(4.5)"],
            "root_support": [{"citation_numbers": [1], "type": "Given"}],
            "problems": problems,
        }],
    }


def test_reason_is_preserved_even_with_zero_remaining() -> None:
    messages = diagnostic_lines(sample_report(["citation is detached"]), None)
    assert "R10ET_R6B_REMAINING=0" in messages
    assert "R10ET_R6B_PROBLEM_1=citation is detached" in messages
    assert "R10ET_R6B_VERDICT=REVIEW_REQUIRED" in messages


def test_trace_provenance_is_reported_without_reinterpreting_it() -> None:
    trace = {
        "root_index": 3, "root_premises": [1, 2],
        "images": [{
            "index": 5, "eligible_for_common_definition": True,
            "actual_canonical_common_definition": False,
            "inference_rule": "other", "given_ancestor_citation_numbers": [],
            "root_ancestor": True,
        }],
        "references": [{
            "number": 1, "locator": "(5.1)", "reachable_from_root": False,
            "directly_attributed_to_given": True,
            "reference_heading_displayed": True,
            "body_marker_displayed": False,
        }],
    }
    messages = diagnostic_lines(sample_report(["mismatch"]), trace)
    assert "R10ET_R6B_IMAGE_5_ELIGIBLE=True" in messages
    assert "R10ET_R6B_IMAGE_5_CANONICAL=False" in messages
    assert "R10ET_R6B_CITATION_1_ROOT=False" in messages


def test_clean_case_remains_clean() -> None:
    messages = diagnostic_lines(sample_report([]), {"images": [], "references": []})
    assert "R10ET_R6B_VERDICT=PASS" in messages


def test_missing_case_is_rejected() -> None:
    with pytest.raises(ValueError, match="one pi_10"):
        diagnostic_lines({"cases": []}, None)


def test_latest_existing_report_is_selected(tmp_path: Path) -> None:
    folder = tmp_path / "phase169_r10et_r6_residual_definition_dependency_audit" / "output" / "20261028_171123_720"
    folder.mkdir(parents=True)
    report = folder / "audit.json"
    report.write_text(json.dumps(sample_report([])), encoding="utf-8")
    assert existing_report(tmp_path, None) == report
    assert existing_report(tmp_path, report) == report


def test_no_report_refuses_without_creating_one(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        existing_report(tmp_path, None)
    assert not (tmp_path / "phase169_r10et_r6_residual_definition_dependency_audit").exists()

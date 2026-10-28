"""Focused, portable checks for the read-only R10ET closeout assertions."""
from __future__ import annotations

from copy import deepcopy

import pytest

from phase169_r10et_closeout_r3_final_readonly_audit.audit import (
    PROBE_NAMES,
    REQUIRED_NAMES,
    review_r6_report,
)


def accepted_report() -> dict:
    cases = []
    for name in sorted(REQUIRED_NAMES | PROBE_NAMES):
        is_required = name in REQUIRED_NAMES
        cases.append({
            "case": name, "required": is_required,
            "passed": True, "status": "complete", "trust": "PASS",
            "remaining_eligible_cited_steps": 0, "problems": [],
            "canonical_image_steps": 4 if name == "pi_10^8" else 0,
            "eligible_image_steps": 4 if name == "pi_10^8" else 0,
            "reference_locators": ["DB prior", "(4.5)"] if name == "pi_10^8" else [],
        })
    return {
        "source_verified": True, "tracked_unchanged": True,
        "required_pass": True, "probes_pass": True,
        "full_pytest_run": False, "cases": cases,
    }


def test_complete_set_has_sixteen_plus_three_verified_cases():
    assert review_r6_report(accepted_report()) == (16, 3)


def test_duplicate_case_is_rejected():
    data = accepted_report()
    data["cases"][-1] = deepcopy(data["cases"][0])
    with pytest.raises(ValueError, match="duplicated"):
        review_r6_report(data)


def test_missing_case_is_rejected():
    data = accepted_report()
    data["cases"].pop()
    with pytest.raises(ValueError, match="nineteen"):
        review_r6_report(data)


def test_unverified_step_is_rejected():
    data = accepted_report()
    data["cases"][0]["trust"] = "REVIEW_REQUIRED"
    with pytest.raises(ValueError, match="not verified"):
        review_r6_report(data)


def test_any_remaining_individual_definition_is_rejected():
    data = accepted_report()
    data["cases"][0]["remaining_eligible_cited_steps"] = 1
    with pytest.raises(ValueError, match="not verified"):
        review_r6_report(data)


def test_detached_pi108_reference_is_rejected():
    data = accepted_report()
    item = next(x for x in data["cases"] if x["case"] == "pi_10^8")
    item["reference_locators"].append("unused DB prior")
    with pytest.raises(ValueError, match=r"pi_10\^8"):
        review_r6_report(data)


def test_phase_full_suite_is_never_marked_as_executed():
    data = accepted_report()
    data["full_pytest_run"] = True
    with pytest.raises(ValueError, match="certification"):
        review_r6_report(data)


def test_missing_source_certification_is_rejected():
    data = accepted_report()
    data["source_verified"] = False
    with pytest.raises(ValueError, match="certification"):
        review_r6_report(data)

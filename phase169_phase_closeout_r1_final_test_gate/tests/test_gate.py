"""Pure regression tests for Phase 169 end-of-phase test gate."""
from __future__ import annotations

from copy import deepcopy

import pytest

from phase169_phase_closeout_r1_final_test_gate.run import (
    FOCUSED_TESTS, PROBES, REQUIRED, REVIEWED_BLOBS, inspect_r6,
    passed_count,
)


def sample_evidence():
    cases = []
    for name in sorted(REQUIRED | PROBES):
        cases.append({
            "case": name, "required": name in REQUIRED,
            "passed": True, "status": "complete", "trust": "PASS",
            "remaining_eligible_cited_steps": 0, "problems": [],
            "eligible_image_steps": 4 if name == "pi_10^8" else 0,
            "canonical_image_steps": 4 if name == "pi_10^8" else 0,
            "reference_locators": (
                ["DB prior: sphere.csv (n=4, k=2) [参考: Proposition 5.3]", "(4.5)"]
                if name == "pi_10^8" else []
            ),
        })
    return {
        "cases": cases, "source_verified": True, "tracked_unchanged": True,
        "required_pass": True, "probes_pass": True, "full_pytest_run": False,
    }


def test_verified_r6_evidence_has_exact_case_count():
    assert inspect_r6(sample_evidence()) == (16, 3)


def test_missing_case_rejected():
    data = sample_evidence()
    data["cases"].pop()
    with pytest.raises(ValueError, match="19 cases"):
        inspect_r6(data)


def test_duplicate_case_rejected():
    data = sample_evidence()
    data["cases"][0] = deepcopy(data["cases"][1])
    with pytest.raises(ValueError, match="Duplicate"):
        inspect_r6(data)


def test_untrusted_case_rejected():
    data = sample_evidence()
    data["cases"][0]["trust"] = "REVIEW_REQUIRED"
    with pytest.raises(ValueError, match="Unverified"):
        inspect_r6(data)


def test_detached_reference_rejected():
    data = sample_evidence()
    next(x for x in data["cases"] if x["case"] == "pi_10^8")["reference_locators"].append("unused")
    with pytest.raises(ValueError, match="Detached"):
        inspect_r6(data)


def test_source_evidence_required():
    data = sample_evidence()
    data["source_verified"] = False
    with pytest.raises(ValueError, match="flags"):
        inspect_r6(data)


def test_passed_count_fails_closed():
    assert passed_count("3500 passed in 54.3s", 0) == 3500
    assert passed_count("18 passed, 2 deselected in 1s", 0) == 18
    assert passed_count("1 failed, 1 passed in 1s", 1) is None
    assert passed_count("no tests ran in 1s", 0) is None


def test_reviewed_scope_has_five_docs_and_eight_sources():
    assert len(REVIEWED_BLOBS) == 13
    assert len([x for x in REVIEWED_BLOBS if x == "README.md" or x.startswith("docs/")]) == 5
    assert len(FOCUSED_TESTS) == 10
    assert len(set(FOCUSED_TESTS)) == 10
    assert all(path.endswith(".py") for path in FOCUSED_TESTS)

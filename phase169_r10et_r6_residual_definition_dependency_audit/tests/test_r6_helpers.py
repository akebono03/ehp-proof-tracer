"""R10ET-R6 pure dependency-report regression tests; no repository needed."""
from __future__ import annotations

from phase169_r10et_r6_residual_definition_dependency_audit.audit import (
    REQUIRED, PROBES, STABLE_TRANSPORT, summarize_dependency,
)


def sample():
    citation_source = {
        "number": 1, "locator": "DB prior: sphere.csv",
        "reachable_from_root": True, "reference_heading_displayed": True,
        "directly_attributed_to_given": True,
    }
    citation_iso = {
        "number": 2, "locator": "(4.5)",
        "reachable_from_root": True, "reference_heading_displayed": True,
        "directly_attributed_to_given": True,
    }
    first = {"index": 0, "type": "Relation", "citation_numbers": [1]}
    second = {"index": 1, "type": "Toda45IsomorphismStatement", "citation_numbers": [2]}
    case = {
        "group": "pi_28^22", "status": "complete", "trust": "PASS",
        "image_common_eligible": 14, "image_actual_common": 14,
        "image_cited_but_common_eligible": 0, "images": 14,
        "root_ancestry_steps": 20,
        "references": [citation_source, citation_iso],
        "root_first_two_premise_support": [first, second],
    }
    old = {
        "references": [{"locator": "DB prior: sphere.csv"}, {"locator": "(4.5)"}],
        "image_actual_common": 14,
        "root_first_two_premise_support": [first, second],
    }
    return case, old


def test_r6_accepts_trusted_canonical_rooted_definition():
    case, baseline = sample()
    row = summarize_dependency(case, baseline, stable_transport=True, required=True)
    assert row["passed"] and row["remaining_eligible_cited_steps"] == 0
    assert row["reference_locators"] == ["DB prior: sphere.csv", "(4.5)"]


def test_r6_refuses_noncanonical_eligible_image_even_without_citation():
    case, baseline = sample()
    case["image_actual_common"] -= 1
    row = summarize_dependency(case, baseline, stable_transport=True, required=True)
    assert not row["passed"]
    assert any("noncanonical" in message for message in row["problems"])


def test_r6_refuses_irrelevant_reference_and_missing_ancestor():
    case, baseline = sample()
    case["references"][1]["reachable_from_root"] = False
    row = summarize_dependency(case, baseline, stable_transport=True, required=True)
    assert not row["passed"]
    assert any("detached" in message for message in row["problems"])


def test_r6_refuses_dropped_toda45_root_evidence():
    case, baseline = sample()
    case["root_first_two_premise_support"][1]["citation_numbers"] = []
    row = summarize_dependency(case, baseline, stable_transport=True, required=True)
    assert not row["passed"]
    assert any("(4.5)" in message for message in row["problems"])


def test_r6_does_not_require_db_prior_for_low_stem():
    case, _ = sample()
    case["references"] = [{
        "locator": "Proposition 5.1", "reachable_from_root": True,
        "reference_heading_displayed": True, "directly_attributed_to_given": True,
    }]
    case["image_common_eligible"] = 0
    case["image_actual_common"] = 0
    row = summarize_dependency(case, baseline=None, stable_transport=False, required=False)
    assert row["passed"]


def test_r6_coverage_is_not_only_one_generator_family():
    assert len(REQUIRED) == 16
    assert set(PROBES).isdisjoint(set(REQUIRED))
    assert (43, 26) in STABLE_TRANSPORT
    assert (22, 6) in STABLE_TRANSPORT
    assert (24, 9) in STABLE_TRANSPORT

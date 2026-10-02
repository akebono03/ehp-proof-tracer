from __future__ import annotations

import ast
import csv
from pathlib import Path

import audit_phase155_r3_2b as audit


def test_attribute_field_pi6_is_not_control_flow():
    source = (
        "def render(statement):\n"
        "  return statement.pi6_4_group_relation\n"
    )

    rows = audit.find_pi6_occurrences(
        source
    )

    assert len(
        rows
    ) == 1
    assert (
        rows[0].classification
        == audit.OCCURRENCE_ATTRIBUTE_FIELD
    )
    assert (
        rows[0].in_control_flow
        is False
    )


def test_pi6_in_if_condition_is_control_flow():
    source = (
        "def render(statement):\n"
        "  if statement.pi6_mode:\n"
        "    return 1\n"
        "  return 0\n"
    )

    rows = audit.find_pi6_occurrences(
        source
    )

    assert len(
        rows
    ) == 1
    assert (
        rows[0].classification
        == audit.OCCURRENCE_CONTROL_FLOW
    )
    assert (
        rows[0].in_control_flow
        is True
    )


def test_pi6_string_literal_is_classified():
    source = (
        "VALUE = 'pi6 special route'\n"
    )

    rows = audit.find_pi6_occurrences(
        source
    )

    assert len(
        rows
    ) == 1
    assert (
        rows[0].classification
        == audit.OCCURRENCE_STRING_LITERAL
    )


def test_needs_review_links_known_failure(
    tmp_path: Path,
):
    path = (
        tmp_path
        / "pairs.csv"
    )
    fieldnames = (
        "candidate_id",
        "decision",
        "older_test_id",
        "newer_test_id",
        "older_outcome",
        "newer_outcome",
        "function_hash_equal",
        "dependency_hash_equal",
    )

    with path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerow(
            {
                "candidate_id": "R3-1",
                "decision": "needs_review",
                "older_test_id": (
                    audit.FAILING_TESTS[
                        0
                    ]
                ),
                "newer_test_id": (
                    "tests/test_x.py::test_x"
                ),
                "older_outcome": "failed",
                "newer_outcome": "passed",
                "function_hash_equal": "True",
                "dependency_hash_equal": "True",
            }
        )

    rows = (
        audit.audit_needs_review(
            path
        )
    )

    assert len(
        rows
    ) == 1
    assert (
        rows[0].review_class
        == audit.REVIEW_FAILURE_LINKED
    )


def test_missing_outcome_without_known_failure_is_source_issue(
    tmp_path: Path,
):
    path = (
        tmp_path
        / "pairs.csv"
    )
    fieldnames = (
        "candidate_id",
        "decision",
        "older_test_id",
        "newer_test_id",
        "older_outcome",
        "newer_outcome",
        "function_hash_equal",
        "dependency_hash_equal",
    )

    with path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerow(
            {
                "candidate_id": "R3-2",
                "decision": "needs_review",
                "older_test_id": (
                    "tests/test_a.py::test_a"
                ),
                "newer_test_id": (
                    "tests/test_b.py::test_b"
                ),
                "older_outcome": "missing",
                "newer_outcome": "passed",
                "function_hash_equal": "False",
                "dependency_hash_equal": "False",
            }
        )

    rows = (
        audit.audit_needs_review(
            path
        )
    )

    assert (
        rows[0].review_class
        == audit.REVIEW_SOURCE_EVIDENCE
    )


def test_non_review_rows_are_ignored(
    tmp_path: Path,
):
    path = (
        tmp_path
        / "pairs.csv"
    )
    fieldnames = (
        "candidate_id",
        "decision",
        "older_test_id",
        "newer_test_id",
        "older_outcome",
        "newer_outcome",
        "function_hash_equal",
        "dependency_hash_equal",
    )

    with path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerow(
            {
                "candidate_id": "R3-3",
                "decision": "retain_independent",
                "older_test_id": (
                    "tests/test_a.py::test_a"
                ),
                "newer_test_id": (
                    "tests/test_b.py::test_b"
                ),
                "older_outcome": "passed",
                "newer_outcome": "passed",
                "function_hash_equal": "False",
                "dependency_hash_equal": "False",
            }
        )

    assert (
        audit.audit_needs_review(
            path
        )
        == []
    )


def test_global_pi6_ban_is_detected_in_test_source(
    tmp_path: Path,
):
    repo = tmp_path
    test_path = (
        repo
        / "tests"
        / "test_phase143_1_generic_proof_order.py"
    )
    test_path.parent.mkdir(
        parents=True,
    )
    test_path.write_text(
        "def test_phase143_1_generic_order_has_no_pi6_specific_hardcoding():\n"
        "  forbidden_fragments = ('pi6',)\n"
        "  for fragment in forbidden_fragments:\n"
        "    assert fragment not in 'source'\n",
        encoding="utf-8",
    )

    source = (
        "def render(statement):\n"
        "  return statement.pi6_4_group_relation\n"
    )
    occurrences = (
        audit.find_pi6_occurrences(
            source
        )
    )

    row = (
        audit.audit_failing_tests(
            repo,
            occurrences,
        )[0]
    )

    assert (
        row.stale_expectation_supported
        is True
    )

from __future__ import annotations

import audit_phase155_r3_2d as audit


def test_normalize_nodeid_strips_parameter_suffix():
    assert (
        audit.normalize_nodeid(
            "tests/test_x.py::test_a[3-3]"
        )
        == "tests/test_x.py::test_a"
    )


def test_normalize_nodeid_preserves_plain_nodeid():
    assert (
        audit.normalize_nodeid(
            "tests\\test_x.py::test_a"
        )
        == "tests/test_x.py::test_a"
    )


def test_parameterized_nodeid_is_detected():
    assert (
        audit.is_parameterized_nodeid(
            "tests/test_x.py::test_a[value]"
        )
        is True
    )
    assert (
        audit.is_parameterized_nodeid(
            "tests/test_x.py::test_a"
        )
        is False
    )


def test_execution_matches_parameterized_instances():
    rows = [
        {
            "test_id": (
                "tests/test_x.py::test_a[one]"
            ),
            "outcome": "passed",
        },
        {
            "test_id": (
                "tests/test_x.py::test_a[two]"
            ),
            "outcome": "passed",
        },
        {
            "test_id": (
                "tests/test_x.py::test_b"
            ),
            "outcome": "passed",
        },
    ]

    matches = audit.execution_matches(
        "tests/test_x.py::test_a",
        rows,
    )

    assert len(
        matches
    ) == 2


def test_parameterized_all_pass_is_recorder_gap():
    missing = audit.MissingTestRecord(
        candidate_id="R3-1",
        requested_test_id=(
            "tests/test_x.py::test_a"
        ),
        pair_side="older",
        original_outcome="missing",
    )
    execution_rows = [
        {
            "test_id": (
                "tests/test_x.py::test_a[one]"
            ),
            "outcome": "passed",
        },
        {
            "test_id": (
                "tests/test_x.py::test_a[two]"
            ),
            "outcome": "passed",
        },
    ]
    collection = audit.CollectionRecord(
        requested_test_id=(
            missing.requested_test_id
        ),
        pytest_exit_code=0,
        collected_nodeids=(
            "tests/test_x.py::test_a[one]"
            "\x1f"
            "tests/test_x.py::test_a[two]"
        ),
        collected_count=2,
        stderr="",
    )

    row = audit.classify_missing(
        missing,
        execution_rows,
        collection,
    )

    assert (
        row.root_cause
        == audit.CAUSE_PARAMETERIZED_ALL_PASS
    )
    assert (
        row.recorder_fix_needed
        is True
    )
    assert (
        row.test_fix_needed
        is False
    )


def test_parameterized_failure_is_test_related():
    missing = audit.MissingTestRecord(
        candidate_id="R3-1",
        requested_test_id=(
            "tests/test_x.py::test_a"
        ),
        pair_side="older",
        original_outcome="missing",
    )
    execution_rows = [
        {
            "test_id": (
                "tests/test_x.py::test_a[one]"
            ),
            "outcome": "passed",
        },
        {
            "test_id": (
                "tests/test_x.py::test_a[two]"
            ),
            "outcome": "failed",
        },
    ]
    collection = audit.CollectionRecord(
        requested_test_id=(
            missing.requested_test_id
        ),
        pytest_exit_code=0,
        collected_nodeids=(
            "tests/test_x.py::test_a[one]"
            "\x1f"
            "tests/test_x.py::test_a[two]"
        ),
        collected_count=2,
        stderr="",
    )

    row = audit.classify_missing(
        missing,
        execution_rows,
        collection,
    )

    assert (
        row.root_cause
        == audit.CAUSE_PARAMETERIZED_HAS_FAILURE
    )
    assert (
        row.test_fix_needed
        is True
    )


def test_collected_without_saved_execution_is_recorder_gap():
    missing = audit.MissingTestRecord(
        candidate_id="R3-1",
        requested_test_id=(
            "tests/test_x.py::test_a"
        ),
        pair_side="older",
        original_outcome="missing",
    )
    collection = audit.CollectionRecord(
        requested_test_id=(
            missing.requested_test_id
        ),
        pytest_exit_code=0,
        collected_nodeids=(
            "tests/test_x.py::test_a[one]"
        ),
        collected_count=1,
        stderr="",
    )

    row = audit.classify_missing(
        missing,
        [],
        collection,
    )

    assert (
        row.root_cause
        == audit.CAUSE_COLLECTED_BUT_NOT_RECORDED
    )
    assert (
        row.recorder_fix_needed
        is True
    )


def test_load_missing_tests_only_selects_missing_sides():
    rows = [
        {
            "candidate_id": "R3-1",
            "root_cause": (
                audit.ROOT_MISSING_EXECUTION
            ),
            "older_test_id": (
                "tests/test_a.py::test_a"
            ),
            "newer_test_id": (
                "tests/test_b.py::test_b"
            ),
            "older_outcome": "missing",
            "newer_outcome": "passed",
        }
    ]

    result = audit.load_missing_tests(
        rows
    )

    assert len(
        result
    ) == 1
    assert (
        result[0].requested_test_id
        == "tests/test_a.py::test_a"
    )

from __future__ import annotations

import audit_phase155_r3_2e as audit


def test_normalize_nodeid_strips_parameter_suffix():
    assert (
        audit.normalize_nodeid(
            "tests/test_x.py::test_a[value]"
        )
        == "tests/test_x.py::test_a"
    )


def test_load_base_tests_deduplicates_twelve_references():
    rows = [
        {
            "requested_test_id": (
                "tests/test_x.py::test_a"
            )
        },
        {
            "requested_test_id": (
                "tests/test_x.py::test_a"
            )
        },
        {
            "requested_test_id": (
                "tests/test_y.py::test_b"
            )
        },
    ]

    result = audit.load_base_tests(
        rows
    )

    assert tuple(
        row.requested_test_id
        for row in result
    ) == (
        "tests/test_x.py::test_a",
        "tests/test_y.py::test_b",
    )


def _recorder(
    collected,
    reports,
):
    recorder = audit.FreshRecorder()
    recorder.collected = list(
        collected
    )
    recorder.reports = list(
        reports
    )
    return recorder


def test_map_instance_reports_maps_parameterized_nodes_to_base():
    base_tests = (
        audit.BaseTest(
            requested_test_id=(
                "tests/test_x.py::test_a"
            )
        ),
    )
    recorder = _recorder(
        [
            "tests/test_x.py::test_a[one]",
            "tests/test_x.py::test_a[two]",
        ],
        [
            (
                "tests/test_x.py::test_a[one]",
                "call",
                "passed",
                0.1,
                "",
            ),
            (
                "tests/test_x.py::test_a[two]",
                "call",
                "passed",
                0.1,
                "",
            ),
        ],
    )

    rows = audit.map_instance_reports(
        base_tests,
        recorder,
    )

    assert len(
        rows
    ) == 2
    assert all(
        row.requested_test_id
        == "tests/test_x.py::test_a"
        for row in rows
    )


def test_all_parameterized_instances_pass_clears_false_failure():
    base_tests = (
        audit.BaseTest(
            requested_test_id=(
                "tests/test_x.py::test_a"
            )
        ),
    )
    recorder = _recorder(
        [
            "tests/test_x.py::test_a[one]",
            "tests/test_x.py::test_a[two]",
        ],
        [
            (
                "tests/test_x.py::test_a[one]",
                "setup",
                "passed",
                0.01,
                "",
            ),
            (
                "tests/test_x.py::test_a[one]",
                "call",
                "passed",
                0.1,
                "",
            ),
            (
                "tests/test_x.py::test_a[two]",
                "setup",
                "passed",
                0.01,
                "",
            ),
            (
                "tests/test_x.py::test_a[two]",
                "call",
                "passed",
                0.1,
                "",
            ),
        ],
    )
    reports = audit.map_instance_reports(
        base_tests,
        recorder,
    )

    rows = audit.decompose(
        base_tests,
        recorder,
        reports,
    )

    assert (
        rows[0].root_cause
        == audit.CAUSE_ALL_INSTANCES_PASS
    )
    assert (
        rows[0].r3_2d_false_failure_classification
        is True
    )
    assert (
        rows[0].blocking
        is False
    )


def test_real_call_failure_remains_blocking():
    base_tests = (
        audit.BaseTest(
            requested_test_id=(
                "tests/test_x.py::test_a"
            )
        ),
    )
    recorder = _recorder(
        [
            "tests/test_x.py::test_a[one]",
            "tests/test_x.py::test_a[two]",
        ],
        [
            (
                "tests/test_x.py::test_a[one]",
                "call",
                "passed",
                0.1,
                "",
            ),
            (
                "tests/test_x.py::test_a[two]",
                "call",
                "failed",
                0.1,
                "failure",
            ),
        ],
    )
    reports = audit.map_instance_reports(
        base_tests,
        recorder,
    )

    rows = audit.decompose(
        base_tests,
        recorder,
        reports,
    )

    assert (
        rows[0].root_cause
        == audit.CAUSE_INSTANCE_FAILURE
    )
    assert (
        rows[0].blocking
        is True
    )


def test_setup_failure_remains_blocking():
    base_tests = (
        audit.BaseTest(
            requested_test_id=(
                "tests/test_x.py::test_a"
            )
        ),
    )
    recorder = _recorder(
        [
            "tests/test_x.py::test_a[one]",
        ],
        [
            (
                "tests/test_x.py::test_a[one]",
                "setup",
                "failed",
                0.1,
                "setup failed",
            ),
        ],
    )
    reports = audit.map_instance_reports(
        base_tests,
        recorder,
    )

    rows = audit.decompose(
        base_tests,
        recorder,
        reports,
    )

    assert (
        rows[0].root_cause
        == audit.CAUSE_SETUP_FAILURE
    )


def test_not_collected_is_blocking():
    base_tests = (
        audit.BaseTest(
            requested_test_id=(
                "tests/test_x.py::test_a"
            )
        ),
    )
    recorder = _recorder(
        [],
        [],
    )

    rows = audit.decompose(
        base_tests,
        recorder,
        [],
    )

    assert (
        rows[0].root_cause
        == audit.CAUSE_NOT_COLLECTED
    )
    assert (
        rows[0].blocking
        is True
    )


def test_collected_without_call_report_is_blocking():
    base_tests = (
        audit.BaseTest(
            requested_test_id=(
                "tests/test_x.py::test_a"
            )
        ),
    )
    recorder = _recorder(
        [
            "tests/test_x.py::test_a[one]",
        ],
        [
            (
                "tests/test_x.py::test_a[one]",
                "setup",
                "passed",
                0.01,
                "",
            ),
        ],
    )
    reports = audit.map_instance_reports(
        base_tests,
        recorder,
    )

    rows = audit.decompose(
        base_tests,
        recorder,
        reports,
    )

    assert (
        rows[0].root_cause
        == audit.CAUSE_NO_CALL_REPORT
    )

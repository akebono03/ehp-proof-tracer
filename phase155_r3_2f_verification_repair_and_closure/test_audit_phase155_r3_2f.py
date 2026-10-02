from __future__ import annotations

import audit_phase155_r3_2f as audit


def test_normalize_nodeid_collapses_parameterized_instance():
    assert (
        audit.normalize_nodeid(
            "tests/test_x.py::test_a[case-1]"
        )
        == "tests/test_x.py::test_a"
    )


def test_aggregate_runtime_marks_all_parameter_instances_passed():
    recorder = audit.Recorder()
    recorder.collected = [
        "tests/test_x.py::test_a[one]",
        "tests/test_x.py::test_a[two]",
    ]
    recorder.reports = [
        (
            "tests/test_x.py::test_a[one]",
            "call",
            "passed",
        ),
        (
            "tests/test_x.py::test_a[two]",
            "call",
            "passed",
        ),
    ]

    rows = audit.aggregate_runtime(
        (
            "tests/test_x.py::test_a",
        ),
        recorder,
    )

    assert len(rows) == 1
    assert (
        rows[0].runtime_status
        == "passed"
    )
    assert rows[0].call_count == 2
    assert rows[0].passed_count == 2


def test_aggregate_runtime_propagates_parameter_failure():
    recorder = audit.Recorder()
    recorder.collected = [
        "tests/test_x.py::test_a[one]",
        "tests/test_x.py::test_a[two]",
    ]
    recorder.reports = [
        (
            "tests/test_x.py::test_a[one]",
            "call",
            "passed",
        ),
        (
            "tests/test_x.py::test_a[two]",
            "call",
            "failed",
        ),
    ]

    rows = audit.aggregate_runtime(
        (
            "tests/test_x.py::test_a",
        ),
        recorder,
    )

    assert (
        rows[0].runtime_status
        == "failed"
    )


def _runtime(test_id: str, status: str = "passed"):
    return audit.RuntimeAggregate(
        requested_test_id=test_id,
        collected_count=1,
        call_count=1,
        passed_count=(
            1
            if status == "passed"
            else 0
        ),
        failed_count=(
            1
            if status == "failed"
            else 0
        ),
        skipped_count=0,
        setup_teardown_failure_count=0,
        runtime_status=status,
    )


def test_exact_pair_with_matching_fingerprints_is_removable():
    candidates = [
        {
            "candidate_id": "R3-1",
            "category": audit.CATEGORY_EXACT,
            "older_test_id": "tests/test_a.py::test_a",
            "newer_test_id": "tests/test_b.py::test_b",
            "older_semantic_atoms": "",
            "newer_semantic_atoms": "",
        }
    ]
    prior = [
        {
            "candidate_id": "R3-1",
            "function_hash_equal": "True",
            "semantic_function_hash_equal": "True",
            "dependency_hash_equal": "True",
            "decision": "needs_review",
        }
    ]
    sources = [
        {
            "test_id": "tests/test_a.py::test_a",
            "source_available": "True",
        },
        {
            "test_id": "tests/test_b.py::test_b",
            "source_available": "True",
        },
    ]
    runtime = [
        _runtime("tests/test_a.py::test_a"),
        _runtime("tests/test_b.py::test_b"),
    ]

    rows = audit.classify_pairs(
        candidates,
        prior,
        sources,
        runtime,
    )

    assert rows[0].decision == audit.DECISION_REMOVABLE


def test_superseded_pair_without_dependency_match_is_retained():
    candidates = [
        {
            "candidate_id": "R3-1",
            "category": audit.CATEGORY_SUPERSEDED,
            "older_test_id": "tests/test_a.py::test_a",
            "newer_test_id": "tests/test_b.py::test_b",
            "older_semantic_atoms": "a\x1fb",
            "newer_semantic_atoms": "a\x1fb\x1fc",
        }
    ]
    prior = [
        {
            "candidate_id": "R3-1",
            "function_hash_equal": "False",
            "semantic_function_hash_equal": "False",
            "dependency_hash_equal": "False",
            "decision": "needs_review",
        }
    ]
    sources = [
        {
            "test_id": "tests/test_a.py::test_a",
            "source_available": "True",
        },
        {
            "test_id": "tests/test_b.py::test_b",
            "source_available": "True",
        },
    ]
    runtime = [
        _runtime("tests/test_a.py::test_a"),
        _runtime("tests/test_b.py::test_b"),
    ]

    rows = audit.classify_pairs(
        candidates,
        prior,
        sources,
        runtime,
    )

    assert rows[0].decision == audit.DECISION_RETAIN


def test_nonpassing_runtime_remains_needs_review():
    candidates = [
        {
            "candidate_id": "R3-1",
            "category": audit.CATEGORY_EXACT,
            "older_test_id": "tests/test_a.py::test_a",
            "newer_test_id": "tests/test_b.py::test_b",
            "older_semantic_atoms": "",
            "newer_semantic_atoms": "",
        }
    ]
    prior = [
        {
            "candidate_id": "R3-1",
            "function_hash_equal": "True",
            "semantic_function_hash_equal": "True",
            "dependency_hash_equal": "True",
            "decision": "needs_review",
        }
    ]
    sources = [
        {
            "test_id": "tests/test_a.py::test_a",
            "source_available": "True",
        },
        {
            "test_id": "tests/test_b.py::test_b",
            "source_available": "True",
        },
    ]
    runtime = [
        _runtime(
            "tests/test_a.py::test_a",
            status="failed",
        ),
        _runtime("tests/test_b.py::test_b"),
    ]

    rows = audit.classify_pairs(
        candidates,
        prior,
        sources,
        runtime,
    )

    assert rows[0].decision == audit.DECISION_REVIEW

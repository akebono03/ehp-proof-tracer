from __future__ import annotations

import ast

import audit_phase155_r3_2f_r1 as audit


def test_normalize_nodeid_collapses_parameterized_instance():
    assert (
        audit.normalize_nodeid(
            "tests/test_x.py::test_a[case]"
        )
        == "tests/test_x.py::test_a"
    )


def test_aggregate_runtime_collects_parameterized_passes():
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

    assert len(
        rows
    ) == 1
    assert (
        rows[0].runtime_status
        == "passed"
    )
    assert rows[0].call_count == 2


def test_dependency_hash_changes_with_import_context():
    tree_a = ast.parse(
        "import inspect\n"
        "def test_x():\n"
        "  assert inspect.getsource\n"
    )
    tree_b = ast.parse(
        "import inspect as other\n"
        "def test_x():\n"
        "  assert other.getsource\n"
    )

    function_a = tree_a.body[
        1
    ]
    function_b = tree_b.body[
        1
    ]

    assert (
        audit._dependency_hash(
            tree_a,
            function_a,
        )
        != audit._dependency_hash(
            tree_b,
            function_b,
        )
    )


def _runtime(
    test_id: str,
    status: str = "passed",
):
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


def _source(
    test_id: str,
    function_hash: str,
    dependency_hash: str,
):
    return audit.SourceEvidence(
        test_id=test_id,
        function_hash=function_hash,
        semantic_function_hash=(
            function_hash
        ),
        dependency_hash=(
            dependency_hash
        ),
        source_available=True,
    )


def test_current_exact_pair_can_be_removable():
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
    runtime = [
        _runtime(
            "tests/test_a.py::test_a"
        ),
        _runtime(
            "tests/test_b.py::test_b"
        ),
    ]
    sources = [
        _source(
            "tests/test_a.py::test_a",
            "same",
            "deps",
        ),
        _source(
            "tests/test_b.py::test_b",
            "same",
            "deps",
        ),
    ]

    rows = audit.classify_pairs(
        candidates,
        runtime,
        sources,
    )

    assert (
        rows[0].decision
        == audit.DECISION_REMOVABLE
    )


def test_current_source_difference_retains_pair():
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
    runtime = [
        _runtime(
            "tests/test_a.py::test_a"
        ),
        _runtime(
            "tests/test_b.py::test_b"
        ),
    ]
    sources = [
        _source(
            "tests/test_a.py::test_a",
            "a",
            "deps",
        ),
        _source(
            "tests/test_b.py::test_b",
            "b",
            "deps",
        ),
    ]

    rows = audit.classify_pairs(
        candidates,
        runtime,
        sources,
    )

    assert (
        rows[0].decision
        == audit.DECISION_RETAIN
    )


def test_nonpassing_runtime_needs_review():
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
    runtime = [
        _runtime(
            "tests/test_a.py::test_a",
            status="failed",
        ),
        _runtime(
            "tests/test_b.py::test_b"
        ),
    ]
    sources = [
        _source(
            "tests/test_a.py::test_a",
            "same",
            "deps",
        ),
        _source(
            "tests/test_b.py::test_b",
            "same",
            "deps",
        ),
    ]

    rows = audit.classify_pairs(
        candidates,
        runtime,
        sources,
    )

    assert (
        rows[0].decision
        == audit.DECISION_REVIEW
    )

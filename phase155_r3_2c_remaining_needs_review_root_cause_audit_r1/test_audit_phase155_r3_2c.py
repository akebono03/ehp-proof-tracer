from __future__ import annotations

import audit_phase155_r3_2c as audit


def _verified(
    candidate_id="R3-1",
    older="tests/test_a.py::test_a",
    newer="tests/test_b.py::test_b",
    older_outcome="passed",
    newer_outcome="passed",
):
    return {
        "candidate_id": candidate_id,
        "candidate_category": "exact_duplicate_candidate",
        "older_test_id": older,
        "newer_test_id": newer,
        "older_outcome": older_outcome,
        "newer_outcome": newer_outcome,
        "function_hash_equal": "True",
        "semantic_function_hash_equal": "True",
        "dependency_hash_equal": "False",
    }


def _review(
    candidate_id="R3-1",
    review_class="source_evidence_issue",
):
    return {
        "candidate_id": candidate_id,
        "review_class": review_class,
    }


def _source(
    test_id: str,
    available="True",
):
    file_name, function_name = test_id.split(
        "::",
        1,
    )
    return {
        "test_id": test_id,
        "file": file_name,
        "function": function_name,
        "source_available": available,
    }


def test_source_evidence_review_rows_are_included():
    older = "tests/test_a.py::test_a"
    newer = "tests/test_b.py::test_b"

    rows = audit.classify_root_causes(
        [
            _verified(
                older=older,
                newer=newer,
            )
        ],
        [
            _review(
                review_class=(
                    audit.REVIEW_SOURCE_EVIDENCE
                )
            )
        ],
        [
            _source(
                older
            ),
            _source(
                newer
            ),
        ],
    )

    assert len(rows) == 1


def test_other_review_rows_are_included():
    older = "tests/test_a.py::test_a"
    newer = "tests/test_b.py::test_b"

    rows = audit.classify_root_causes(
        [
            _verified(
                older=older,
                newer=newer,
            )
        ],
        [
            _review(
                review_class=(
                    audit.REVIEW_OTHER
                )
            )
        ],
        [
            _source(
                older
            ),
            _source(
                newer
            ),
        ],
    )

    assert len(rows) == 1


def test_failure_linked_rows_are_already_resolved_and_skipped():
    rows = audit.classify_root_causes(
        [],
        [
            _review(
                review_class=(
                    audit.REVIEW_FAILURE_LINKED
                )
            )
        ],
        [],
    )

    assert rows == []


def test_known_stale_failure_is_linked():
    failing = next(
        iter(
            audit.FAILING_TESTS
        )
    )
    newer = "tests/test_b.py::test_b"

    rows = audit.classify_root_causes(
        [
            _verified(
                older=failing,
                newer=newer,
                older_outcome="failed",
            )
        ],
        [
            _review()
        ],
        [
            _source(
                failing
            ),
            _source(
                newer
            ),
        ],
    )

    assert (
        rows[0].root_cause
        == audit.ROOT_FAILED_MEMBER
    )


def test_missing_execution_is_detected():
    older = "tests/test_a.py::test_a"
    newer = "tests/test_b.py::test_b"

    rows = audit.classify_root_causes(
        [
            _verified(
                older=older,
                newer=newer,
                older_outcome="missing",
            )
        ],
        [
            _review()
        ],
        [
            _source(
                older
            ),
            _source(
                newer
            ),
        ],
    )

    assert (
        rows[0].root_cause
        == audit.ROOT_MISSING_EXECUTION
    )


def test_false_source_available_is_detected():
    older = "tests/test_a.py::test_a"
    newer = "tests/test_b.py::test_b"

    rows = audit.classify_root_causes(
        [
            _verified(
                older=older,
                newer=newer,
            )
        ],
        [
            _review()
        ],
        [
            _source(
                older,
                available="False",
            ),
            _source(
                newer
            ),
        ],
    )

    assert (
        rows[0].root_cause
        == audit.ROOT_SOURCE_UNAVAILABLE
    )


def test_passing_pair_with_source_is_conservative_retain():
    older = "tests/test_a.py::test_a"
    newer = "tests/test_b.py::test_b"

    rows = audit.classify_root_causes(
        [
            _verified(
                older=older,
                newer=newer,
            )
        ],
        [
            _review()
        ],
        [
            _source(
                older
            ),
            _source(
                newer
            ),
        ],
    )

    assert (
        rows[0].root_cause
        == audit.ROOT_CLASSIFIER_CONSERVATIVE
    )

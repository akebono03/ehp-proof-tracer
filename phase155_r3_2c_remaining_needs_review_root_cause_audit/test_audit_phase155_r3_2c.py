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
):
    return {
        "candidate_id": candidate_id,
        "review_class": "other_review_reason",
    }


def _source(
    test_id: str,
    available="True",
):
    file_name, function_name = (
        test_id.split(
            "::",
            1,
        )
    )
    return {
        "test_id": test_id,
        "file": file_name,
        "function": function_name,
        "source_available": available,
    }


def test_known_failed_member_is_stale_failure_linked():
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


def test_missing_execution_is_blocking_root_cause():
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


def test_source_unavailable_is_blocking_root_cause():
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


def test_passing_pair_with_source_is_conservative_boundary():
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


def test_non_other_review_rows_are_ignored():
    rows = audit.classify_root_causes(
        [
            _verified()
        ],
        [
            {
                "candidate_id": "R3-1",
                "review_class": "failure_linked",
            }
        ],
        [
            _source(
                "tests/test_a.py::test_a"
            ),
            _source(
                "tests/test_b.py::test_b"
            ),
        ],
    )

    assert rows == []


def test_only_six_other_rows_are_expected_from_real_r3_2b_contract():
    reviews = [
        {
            "candidate_id": f"R3-{index}",
            "review_class": "other_review_reason",
        }
        for index in range(
            6
        )
    ]

    verified = []
    sources = []

    for index in range(
        6
    ):
        older = (
            f"tests/test_{index}a.py::test_a"
        )
        newer = (
            f"tests/test_{index}b.py::test_b"
        )

        verified.append(
            _verified(
                candidate_id=(
                    f"R3-{index}"
                ),
                older=older,
                newer=newer,
            )
        )
        sources.extend(
            (
                _source(
                    older
                ),
                _source(
                    newer
                ),
            )
        )

    rows = audit.classify_root_causes(
        verified,
        reviews,
        sources,
    )

    assert len(
        rows
    ) == 6

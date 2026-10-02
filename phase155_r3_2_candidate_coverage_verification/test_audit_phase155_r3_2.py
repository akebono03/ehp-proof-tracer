from __future__ import annotations

import ast

import audit_phase155_r3_2 as r3


def _pair(
    category: str,
) -> r3.CandidatePair:
    return r3.CandidatePair(
        candidate_id="R3-1",
        category=category,
        older_test_id=(
            "tests/test_phase100_x.py::test_old"
        ),
        newer_test_id=(
            "tests/test_phase154_x.py::test_new"
        ),
        older_phase="100",
        newer_phase="154",
        shared_call_surface="render",
        older_semantic_atoms=(
            "str:a\x1fstr:b"
        ),
        newer_semantic_atoms=(
            "str:a\x1fstr:b\x1fstr:c"
        ),
        evidence="candidate",
        deletion_authorized="False",
    )


def _execution(
    test_id: str,
    outcome: str = "passed",
) -> r3.TestExecution:
    return r3.TestExecution(
        test_id=test_id,
        outcome=outcome,
        duration_seconds=0.1,
        longrepr="",
    )


def _source(
    test_id: str,
    function_hash: str = "f",
    semantic_hash: str = "s",
    dependency_hash: str = "d",
) -> r3.SourceEvidence:
    file_name, function_name = (
        test_id.split(
            "::",
            1,
        )
    )

    return r3.SourceEvidence(
        test_id=test_id,
        file=file_name,
        function=function_name,
        function_hash=function_hash,
        semantic_function_hash=(
            semantic_hash
        ),
        dependency_hash=(
            dependency_hash
        ),
        dependency_symbols=(
            "render"
        ),
        source_available=True,
        source_error="",
    )


def test_unique_test_ids_deduplicates_pair_members():
    pairs = [
        _pair(
            r3.CATEGORY_EXACT
        ),
        _pair(
            r3.CATEGORY_SUPERSEDED
        ),
    ]

    assert (
        r3.unique_test_ids(
            pairs
        )
        == (
            "tests/test_phase100_x.py::test_old",
            "tests/test_phase154_x.py::test_new",
        )
    )


def test_exact_pair_requires_equal_dependency_context():
    pair = _pair(
        r3.CATEGORY_EXACT
    )

    older_execution = _execution(
        pair.older_test_id
    )
    newer_execution = _execution(
        pair.newer_test_id
    )

    decision, _, authorized = (
        r3.classify_pair(
            pair,
            older_execution,
            newer_execution,
            _source(
                pair.older_test_id,
                function_hash="same",
                dependency_hash="old",
            ),
            _source(
                pair.newer_test_id,
                function_hash="same",
                dependency_hash="new",
            ),
        )
    )

    assert (
        decision
        == r3.DECISION_RETAIN
    )
    assert authorized is False


def test_exact_pair_is_removable_when_body_and_dependencies_match():
    pair = _pair(
        r3.CATEGORY_EXACT
    )

    decision, _, authorized = (
        r3.classify_pair(
            pair,
            _execution(
                pair.older_test_id
            ),
            _execution(
                pair.newer_test_id
            ),
            _source(
                pair.older_test_id,
                function_hash="same",
                dependency_hash="same",
            ),
            _source(
                pair.newer_test_id,
                function_hash="same",
                dependency_hash="same",
            ),
        )
    )

    assert (
        decision
        == r3.DECISION_REMOVABLE
    )
    assert authorized is True


def test_superseded_pair_requires_atom_superset_and_dependency_match():
    pair = _pair(
        r3.CATEGORY_SUPERSEDED
    )

    decision, _, authorized = (
        r3.classify_pair(
            pair,
            _execution(
                pair.older_test_id
            ),
            _execution(
                pair.newer_test_id
            ),
            _source(
                pair.older_test_id,
                dependency_hash="same",
            ),
            _source(
                pair.newer_test_id,
                dependency_hash="same",
            ),
        )
    )

    assert (
        decision
        == r3.DECISION_REMOVABLE
    )
    assert authorized is True


def test_failed_candidate_is_needs_review():
    pair = _pair(
        r3.CATEGORY_EXACT
    )

    decision, _, authorized = (
        r3.classify_pair(
            pair,
            _execution(
                pair.older_test_id,
                outcome="failed",
            ),
            _execution(
                pair.newer_test_id,
            ),
            _source(
                pair.older_test_id,
            ),
            _source(
                pair.newer_test_id,
            ),
        )
    )

    assert (
        decision
        == r3.DECISION_REVIEW
    )
    assert authorized is False


def test_historical_name_forces_historical_keep():
    pair = r3.CandidatePair(
        candidate_id="R3-h",
        category=r3.CATEGORY_EXACT,
        older_test_id=(
            "tests/test_phase100_x.py::test_legacy_route"
        ),
        newer_test_id=(
            "tests/test_phase154_x.py::test_new"
        ),
        older_phase="100",
        newer_phase="154",
        shared_call_surface="render",
        older_semantic_atoms="str:a",
        newer_semantic_atoms="str:a",
        evidence="candidate",
        deletion_authorized="False",
    )

    decision, _, authorized = (
        r3.classify_pair(
            pair,
            _execution(
                pair.older_test_id
            ),
            _execution(
                pair.newer_test_id
            ),
            _source(
                pair.older_test_id,
            ),
            _source(
                pair.newer_test_id,
            ),
        )
    )

    assert (
        decision
        == r3.DECISION_HISTORICAL
    )
    assert authorized is False


def test_dependency_signature_changes_when_helper_definition_changes():
    tree_a = ast.parse(
        "def helper():\n"
        "  return 1\n\n"
        "def test_x():\n"
        "  assert helper() == 1\n"
    )
    tree_b = ast.parse(
        "def helper():\n"
        "  return 2\n\n"
        "def test_x():\n"
        "  assert helper() == 1\n"
    )

    function_a = (
        tree_a.body[1]
    )
    function_b = (
        tree_b.body[1]
    )

    hash_a, symbols_a = (
        r3._dependency_signature(
            tree_a,
            function_a,
        )
    )
    hash_b, symbols_b = (
        r3._dependency_signature(
            tree_b,
            function_b,
        )
    )

    assert symbols_a == (
        "helper",
    )
    assert symbols_b == (
        "helper",
    )
    assert hash_a != hash_b


def test_dependency_signature_matches_identical_import_context():
    tree_a = ast.parse(
        "from x import render\n\n"
        "def test_a():\n"
        "  assert render() == 'x'\n"
    )
    tree_b = ast.parse(
        "from x import render\n\n"
        "def test_b():\n"
        "  assert render() == 'x'\n"
    )

    hash_a, _ = (
        r3._dependency_signature(
            tree_a,
            tree_a.body[1],
        )
    )
    hash_b, _ = (
        r3._dependency_signature(
            tree_b,
            tree_b.body[1],
        )
    )

    assert hash_a == hash_b

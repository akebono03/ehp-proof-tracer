from __future__ import annotations

import ast

import audit_phase155_r3_1 as r3


def _function(source: str):
    tree = ast.parse(source)
    return tree.body[0]


def test_old_phase_number_alone_does_not_make_superseded():
    records = [
        r3.TestRecord(
            test_id="tests/test_phase100_x.py::test_old",
            file="tests/test_phase100_x.py",
            function="test_old",
            phase="100",
            line=1,
            exact_hash="a",
            semantic_hash="a",
            call_surface="render",
            assertion_atoms="str:old",
            semantic_atoms="str:old",
            assertion_count=1,
            primary_category=r3.CATEGORY_INDEPENDENT,
            category_reason="",
        ),
        r3.TestRecord(
            test_id="tests/test_phase154_x.py::test_new",
            file="tests/test_phase154_x.py",
            function="test_new",
            phase="154",
            line=1,
            exact_hash="b",
            semantic_hash="b",
            call_surface="render",
            assertion_atoms="str:new",
            semantic_atoms="str:new",
            assertion_count=1,
            primary_category=r3.CATEGORY_INDEPENDENT,
            category_reason="",
        ),
    ]

    pairs = r3.build_pair_candidates(
        records
    )

    assert pairs == []


def test_semantic_string_normalizes_punctuation():
    assert (
        r3._normalize_string(
            "まず、結論。"
        )
        == "まず, 結論."
    )


def test_exact_hash_ignores_test_function_name():
    first = _function(
        "def test_a():\n"
        "  assert run() == 'x'\n"
    )
    second = _function(
        "def test_b():\n"
        "  assert run() == 'x'\n"
    )

    assert (
        r3._hash_function(
            first,
            semantic=False,
        )
        == r3._hash_function(
            second,
            semantic=False,
        )
    )


def test_semantic_hash_collapses_punctuation_only_difference():
    first = _function(
        "def test_a():\n"
        "  assert render() == 'まず、結論。'\n"
    )
    second = _function(
        "def test_b():\n"
        "  assert render() == 'まず, 結論.'\n"
    )

    assert (
        r3._hash_function(
            first,
            semantic=True,
        )
        == r3._hash_function(
            second,
            semantic=True,
        )
    )


def test_superseded_requires_same_call_surface_and_atom_superset():
    older = r3.TestRecord(
        test_id="tests/test_phase100_x.py::test_old",
        file="tests/test_phase100_x.py",
        function="test_old",
        phase="100",
        line=1,
        exact_hash="old",
        semantic_hash="old",
        call_surface="render",
        assertion_atoms="str:a\x1fstr:b",
        semantic_atoms="str:a\x1fstr:b",
        assertion_count=2,
        primary_category=r3.CATEGORY_INDEPENDENT,
        category_reason="",
    )
    newer = r3.TestRecord(
        test_id="tests/test_phase154_x.py::test_new",
        file="tests/test_phase154_x.py",
        function="test_new",
        phase="154",
        line=1,
        exact_hash="new",
        semantic_hash="new",
        call_surface="render",
        assertion_atoms="str:a\x1fstr:b\x1fstr:c",
        semantic_atoms="str:a\x1fstr:b\x1fstr:c",
        assertion_count=3,
        primary_category=r3.CATEGORY_INDEPENDENT,
        category_reason="",
    )

    pairs = r3.build_pair_candidates(
        [older, newer]
    )

    assert len(pairs) == 1
    assert (
        pairs[0].category
        == r3.CATEGORY_SUPERSEDED
    )
    assert (
        pairs[0].deletion_authorized
        is False
    )


def test_different_call_surface_is_not_superseded():
    older = r3.TestRecord(
        test_id="tests/test_phase100_x.py::test_old",
        file="tests/test_phase100_x.py",
        function="test_old",
        phase="100",
        line=1,
        exact_hash="old",
        semantic_hash="old",
        call_surface="render_a",
        assertion_atoms="str:a\x1fstr:b",
        semantic_atoms="str:a\x1fstr:b",
        assertion_count=2,
        primary_category=r3.CATEGORY_INDEPENDENT,
        category_reason="",
    )
    newer = r3.TestRecord(
        test_id="tests/test_phase154_x.py::test_new",
        file="tests/test_phase154_x.py",
        function="test_new",
        phase="154",
        line=1,
        exact_hash="new",
        semantic_hash="new",
        call_surface="render_b",
        assertion_atoms="str:a\x1fstr:b\x1fstr:c",
        semantic_atoms="str:a\x1fstr:b\x1fstr:c",
        assertion_count=3,
        primary_category=r3.CATEGORY_INDEPENDENT,
        category_reason="",
    )

    assert (
        r3.build_pair_candidates(
            [older, newer]
        )
        == []
    )


def test_historical_name_is_explicit_only():
    assert (
        r3._historical_by_name(
            "tests/test_x.py::test_legacy_route"
        )
        is True
    )
    assert (
        r3._historical_by_name(
            "tests/test_phase100_x.py::test_old"
        )
        is False
    )

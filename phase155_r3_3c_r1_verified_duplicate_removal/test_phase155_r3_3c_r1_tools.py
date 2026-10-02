from __future__ import annotations

import ast

import apply_phase155_r3_3c_r1 as apply_tool
import verify_phase155_r3_3c_r1 as verify_tool


def test_matching_top_level_functions_can_return_duplicate_definitions():
    tree = ast.parse(
        "def test_x():\n"
        "  assert True\n"
        "\n"
        "def test_x():\n"
        "  assert True\n"
    )

    matches = (
        apply_tool._matching_top_level_functions(
            tree,
            "test_x",
        )
    )

    assert len(
        matches
    ) == 2


def test_render_without_functions_removes_all_duplicate_definitions():
    source = (
        "def test_x():\n"
        "  assert True\n"
        "\n"
        "def test_x():\n"
        "  assert True\n"
        "\n"
        "def test_keep():\n"
        "  assert True\n"
    )

    new_source, counts = (
        apply_tool._render_without_functions(
            source,
            {
                "test_x"
            },
        )
    )

    assert (
        "def test_x"
        not in new_source
    )
    assert (
        "def test_keep"
        in new_source
    )
    assert counts[
        "test_x"
    ] == 2
    ast.parse(
        new_source
    )


def test_render_without_functions_fails_before_write_when_target_missing():
    source = (
        "def test_keep():\n"
        "  assert True\n"
    )

    try:
        apply_tool._render_without_functions(
            source,
            {
                "test_missing"
            },
        )
    except RuntimeError as exc:
        assert (
            "candidate top-level function not found"
            in str(
                exc
            )
        )
    else:
        raise AssertionError(
            "expected RuntimeError"
        )


def test_function_span_includes_decorator():
    tree = ast.parse(
        "@decorator\n"
        "def test_x():\n"
        "  assert True\n"
    )
    function = tree.body[
        0
    ]

    assert (
        apply_tool._function_span(
            function
        )
        == (
            1,
            3,
        )
    )


def test_survivor_test_ids_excludes_deletion_candidates():
    rows = [
        {
            "test_id": (
                "tests/test_a.py::test_a"
            ),
            "deletion_candidate": (
                "True"
            ),
        },
        {
            "test_id": (
                "tests/test_b.py::test_b"
            ),
            "deletion_candidate": (
                "False"
            ),
        },
    ]

    assert (
        verify_tool._survivor_test_ids(
            rows
        )
        == [
            "tests/test_b.py::test_b"
        ]
    )


def test_top_level_test_names_reports_duplicate_names():
    from pathlib import Path
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        path = (
            Path(
                temp_dir
            )
            / "test_x.py"
        )
        path.write_text(
            "def test_x():\n"
            "  assert True\n"
            "\n"
            "def test_x():\n"
            "  assert True\n",
            encoding="utf-8",
        )

        assert (
            verify_tool._top_level_test_names(
                path
            )
            == [
                "test_x",
                "test_x",
            ]
        )

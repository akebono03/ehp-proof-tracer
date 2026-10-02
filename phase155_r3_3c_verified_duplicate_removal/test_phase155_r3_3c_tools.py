from __future__ import annotations

import ast
from pathlib import Path

import apply_phase155_r3_3c as apply_tool
import verify_phase155_r3_3c as verify_tool


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


def test_remove_functions_preserves_other_tests_and_helpers(
    tmp_path,
):
    path = (
        tmp_path
        / "test_x.py"
    )
    path.write_text(
        "def helper():\n"
        "  return 1\n"
        "\n"
        "def test_delete():\n"
        "  assert helper() == 1\n"
        "\n"
        "def test_keep():\n"
        "  assert helper() == 1\n",
        encoding="utf-8",
    )

    apply_tool._remove_functions(
        path,
        {
            "test_delete"
        },
    )

    source = path.read_text(
        encoding="utf-8",
    )

    assert "def test_delete" not in source
    assert "def helper" in source
    assert "def test_keep" in source
    ast.parse(
        source
    )


def test_remove_multiple_functions_from_same_file(
    tmp_path,
):
    path = (
        tmp_path
        / "test_x.py"
    )
    path.write_text(
        "def test_a():\n"
        "  assert True\n"
        "\n"
        "def test_b():\n"
        "  assert True\n"
        "\n"
        "def test_c():\n"
        "  assert True\n",
        encoding="utf-8",
    )

    apply_tool._remove_functions(
        path,
        {
            "test_a",
            "test_b",
        },
    )

    source = path.read_text(
        encoding="utf-8",
    )

    assert "def test_a" not in source
    assert "def test_b" not in source
    assert "def test_c" in source


def test_top_level_test_names_reads_remaining_tests(
    tmp_path,
):
    path = (
        tmp_path
        / "test_x.py"
    )
    path.write_text(
        "def helper():\n"
        "  pass\n"
        "\n"
        "def test_a():\n"
        "  pass\n",
        encoding="utf-8",
    )

    assert (
        verify_tool._top_level_test_names(
            path
        )
        == {
            "test_a"
        }
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


def test_import_fields_extract_source_file():
    rows = [
        {
            "external_symbol_imports": (
                "tests/test_b.py:helper"
            ),
            "whole_module_importers": "",
        },
        {
            "external_symbol_imports": "",
            "whole_module_importers": (
                "tools/audit_x.py"
            ),
        },
    ]

    assert (
        verify_tool._python_files_from_import_fields(
            rows
        )
        == [
            "tests/test_b.py",
            "tools/audit_x.py",
        ]
    )

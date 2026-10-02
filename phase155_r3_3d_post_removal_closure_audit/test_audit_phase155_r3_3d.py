
from __future__ import annotations

import ast
from collections import Counter

import audit_phase155_r3_3d as audit


def test_top_level_test_counts_detects_duplicate_definition():
    tree = ast.parse(
        "def test_x():\n"
        "  pass\n"
        "\n"
        "def test_x():\n"
        "  pass\n"
        "\n"
        "def helper():\n"
        "  pass\n"
    )

    assert (
        audit._top_level_test_counts(
            tree
        )
        == Counter(
            {
                "test_x": 2,
            }
        )
    )


def test_split_test_id_normalizes_path():
    assert (
        audit._split_test_id(
            r"tests\test_x.py::test_y"
        )
        == (
            "tests/test_x.py",
            "test_y",
        )
    )


def test_locate_reports_missing_file(
    tmp_path,
):
    location = audit._locate(
        tmp_path,
        "tests/test_missing.py::test_x",
        {},
    )

    assert location.file_exists is False
    assert location.exists is False
    assert (
        location.function_definition_count
        == 0
    )


def test_locate_reports_existing_function(
    tmp_path,
):
    tests_dir = (
        tmp_path
        / "tests"
    )
    tests_dir.mkdir()
    path = (
        tests_dir
        / "test_x.py"
    )
    path.write_text(
        "def test_y():\n"
        "  pass\n",
        encoding="utf-8",
    )
    tree = audit._parse_test_file(
        path
    )
    counts = {
        "tests/test_x.py": (
            audit._top_level_test_counts(
                tree
            )
        )
    }

    location = audit._locate(
        tmp_path,
        "tests/test_x.py::test_y",
        counts,
    )

    assert location.file_exists is True
    assert location.exists is True
    assert (
        location.function_definition_count
        == 1
    )


def test_pair_closure_marks_removed_endpoint_as_resolved(
    tmp_path,
):
    tests_dir = (
        tmp_path
        / "tests"
    )
    tests_dir.mkdir()
    path = (
        tests_dir
        / "test_new.py"
    )
    path.write_text(
        "def test_new():\n"
        "  pass\n",
        encoding="utf-8",
    )
    counts = {
        "tests/test_new.py": Counter(
            {
                "test_new": 1,
            }
        )
    }

    rows = audit._pair_closure_rows(
        tmp_path,
        [
            {
                "candidate_id": "C1",
                "decision": (
                    audit.REMOVABLE
                ),
                "older_test_id": (
                    "tests/test_old.py::test_old"
                ),
                "newer_test_id": (
                    "tests/test_new.py::test_new"
                ),
            }
        ],
        counts,
    )

    assert (
        rows[
            0
        ].closure_status
        == "resolved_removable_pair"
    )


def test_pair_closure_requires_historical_endpoints(
    tmp_path,
):
    rows = audit._pair_closure_rows(
        tmp_path,
        [
            {
                "candidate_id": "C1",
                "decision": (
                    audit.HISTORICAL
                ),
                "older_test_id": (
                    "tests/test_a.py::test_a"
                ),
                "newer_test_id": (
                    "tests/test_b.py::test_b"
                ),
            }
        ],
        {},
    )

    assert (
        rows[
            0
        ].closure_status
        == "historical_missing"
    )

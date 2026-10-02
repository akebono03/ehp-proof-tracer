from __future__ import annotations

from pathlib import Path

import audit_phase155_r3_3b as audit


def _write(
    root: Path,
    relative: str,
    content: str,
) -> None:
    path = root / relative
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    path.write_text(
        content,
        encoding="utf-8",
    )


def test_function_only_when_file_has_retained_test(
    tmp_path,
):
    _write(
        tmp_path,
        "tests/test_phase100_a.py",
        "def test_old():\n"
        "  assert True\n"
        "\n"
        "def test_keep():\n"
        "  assert True\n",
    )

    candidates, files = (
        audit.build_safety_audit(
            tmp_path,
            [
                {
                    "test_id": (
                        "tests/test_phase100_a.py::test_old"
                    )
                }
            ],
        )
    )

    assert (
        candidates[
            0
        ].function_status
        == audit.FUNCTION_SAFE
    )
    assert (
        files[
            0
        ].file_status
        == audit.FILE_FUNCTION_ONLY
    )


def test_whole_file_safe_when_all_tests_are_candidates(
    tmp_path,
):
    _write(
        tmp_path,
        "tests/test_phase100_a.py",
        "def helper():\n"
        "  return 1\n"
        "\n"
        "def test_old():\n"
        "  assert helper() == 1\n",
    )

    candidates, files = (
        audit.build_safety_audit(
            tmp_path,
            [
                {
                    "test_id": (
                        "tests/test_phase100_a.py::test_old"
                    )
                }
            ],
        )
    )

    assert (
        candidates[
            0
        ].function_status
        == audit.FUNCTION_SAFE
    )
    assert (
        files[
            0
        ].file_status
        == audit.FILE_SAFE
    )


def test_symbol_import_blocks_whole_file_but_not_test_function(
    tmp_path,
):
    _write(
        tmp_path,
        "tests/test_phase100_a.py",
        "def helper():\n"
        "  return 1\n"
        "\n"
        "def test_old():\n"
        "  assert True\n",
    )
    _write(
        tmp_path,
        "tests/test_phase101_b.py",
        "from tests.test_phase100_a import helper\n"
        "\n"
        "def test_b():\n"
        "  assert helper() == 1\n",
    )

    candidates, files = (
        audit.build_safety_audit(
            tmp_path,
            [
                {
                    "test_id": (
                        "tests/test_phase100_a.py::test_old"
                    )
                }
            ],
        )
    )

    assert (
        candidates[
            0
        ].function_status
        == audit.FUNCTION_SAFE
    )
    assert (
        files[
            0
        ].file_status
        == audit.FILE_BLOCKED_EXTERNAL
    )


def test_direct_import_of_candidate_test_blocks_function_deletion(
    tmp_path,
):
    _write(
        tmp_path,
        "tests/test_phase100_a.py",
        "def test_old():\n"
        "  assert True\n",
    )
    _write(
        tmp_path,
        "tests/test_phase101_b.py",
        "from tests.test_phase100_a import test_old\n"
        "\n"
        "def test_b():\n"
        "  test_old()\n",
    )

    candidates, files = (
        audit.build_safety_audit(
            tmp_path,
            [
                {
                    "test_id": (
                        "tests/test_phase100_a.py::test_old"
                    )
                }
            ],
        )
    )

    assert (
        candidates[
            0
        ].function_status
        == audit.FUNCTION_BLOCKED_EXTERNAL
    )
    assert (
        files[
            0
        ].file_status
        == audit.FILE_BLOCKED_EXTERNAL
    )


def test_module_import_blocks_whole_file(
    tmp_path,
):
    _write(
        tmp_path,
        "tests/test_phase100_a.py",
        "def test_old():\n"
        "  assert True\n",
    )
    _write(
        tmp_path,
        "tests/test_phase101_b.py",
        "import tests.test_phase100_a as old_tests\n"
        "\n"
        "def test_b():\n"
        "  assert old_tests is not None\n",
    )

    _candidates, files = (
        audit.build_safety_audit(
            tmp_path,
            [
                {
                    "test_id": (
                        "tests/test_phase100_a.py::test_old"
                    )
                }
            ],
        )
    )

    assert (
        files[
            0
        ].file_status
        == audit.FILE_BLOCKED_EXTERNAL
    )


def test_missing_candidate_function_is_reported(
    tmp_path,
):
    _write(
        tmp_path,
        "tests/test_phase100_a.py",
        "def test_actual():\n"
        "  assert True\n",
    )

    candidates, _files = (
        audit.build_safety_audit(
            tmp_path,
            [
                {
                    "test_id": (
                        "tests/test_phase100_a.py::test_missing"
                    )
                }
            ],
        )
    )

    assert (
        candidates[
            0
        ].function_status
        == audit.FUNCTION_MISSING
    )


def test_constants_and_helpers_are_counted(
    tmp_path,
):
    _write(
        tmp_path,
        "tests/test_phase100_a.py",
        "CASES = ((1, 2),)\n"
        "\n"
        "def helper():\n"
        "  return CASES\n"
        "\n"
        "def test_old():\n"
        "  assert helper()\n",
    )

    candidates, files = (
        audit.build_safety_audit(
            tmp_path,
            [
                {
                    "test_id": (
                        "tests/test_phase100_a.py::test_old"
                    )
                }
            ],
        )
    )

    assert (
        candidates[
            0
        ].module_helper_count
        == 1
    )
    assert (
        candidates[
            0
        ].module_constant_count
        == 1
    )
    assert (
        files[
            0
        ].constant_count
        == 1
    )

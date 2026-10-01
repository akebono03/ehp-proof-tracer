from __future__ import annotations

import csv
from pathlib import Path

from audit_phase155_r1 import (
    CATEGORY_AUDIT,
    CATEGORY_CURRENT,
    CATEGORY_DUPLICATE,
    CATEGORY_HEAVY,
    CATEGORY_HISTORICAL,
    CATEGORY_SNAPSHOT,
    collect_inventory,
    write_csv,
)


def _write_test_file(repo_root: Path, name: str, source: str) -> None:
    tests_dir = repo_root / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    (tests_dir / name).write_text(source, encoding="utf-8")


def test_phase155_r1_old_phase_number_alone_remains_current_contract(tmp_path: Path):
    _write_test_file(
        tmp_path,
        "test_phase27_example.py",
        "def test_basic_contract():\n    assert 1 + 1 == 2\n",
    )

    rows, _, _ = collect_inventory(tmp_path)

    assert len(rows) == 1
    assert rows[0].primary_category == CATEGORY_CURRENT


def test_phase155_r1_explicit_audit_name_is_audit_only(tmp_path: Path):
    _write_test_file(
        tmp_path,
        "test_phase154_example.py",
        "def test_cross_group_audit():\n    assert True\n",
    )

    rows, _, _ = collect_inventory(tmp_path)

    assert rows[0].primary_category == CATEGORY_AUDIT


def test_phase155_r1_snapshot_requires_snapshot_signal_and_numeric_assert(tmp_path: Path):
    _write_test_file(
        tmp_path,
        "test_phase144_fixed_count_snapshot.py",
        "def test_fixed_count_snapshot():\n    items = [1, 2, 3]\n    assert len(items) == 3\n",
    )

    rows, _, _ = collect_inventory(tmp_path)

    assert rows[0].primary_category == CATEGORY_SNAPSHOT


def test_phase155_r1_historical_signal_is_classified_without_phase_assumption(tmp_path: Path):
    _write_test_file(
        tmp_path,
        "test_legacy_compatibility.py",
        "def test_legacy_compatibility():\n    assert True\n",
    )

    rows, _, _ = collect_inventory(tmp_path)

    assert rows[0].primary_category == CATEGORY_HISTORICAL


def test_phase155_r1_heavy_integration_requires_heavy_signal_and_structural_evidence(tmp_path: Path):
    _write_test_file(
        tmp_path,
        "test_phase150_repository_wide.py",
        "def test_repository_wide():\n    for value in range(3):\n        assert value >= 0\n",
    )

    rows, _, _ = collect_inventory(tmp_path)

    assert rows[0].primary_category == CATEGORY_HEAVY


def test_phase155_r1_exact_normalized_ast_duplicates_are_detected(tmp_path: Path):
    _write_test_file(
        tmp_path,
        "test_a.py",
        "def test_alpha():\n    value = 2 + 2\n    assert value == 4\n",
    )
    _write_test_file(
        tmp_path,
        "test_b.py",
        "def test_beta():\n    value = 2 + 2\n    assert value == 4\n",
    )

    rows, _, groups = collect_inventory(tmp_path)

    assert len(groups) == 1
    assert {row.primary_category for row in rows} == {CATEGORY_DUPLICATE}


def test_phase155_r1_csv_contains_replaceable_inventory_fields(tmp_path: Path):
    _write_test_file(
        tmp_path,
        "test_example.py",
        "def test_contract():\n    assert True\n",
    )
    rows, _, _ = collect_inventory(tmp_path)
    output = tmp_path / "inventory.csv"

    write_csv(output, rows)

    with output.open("r", encoding="utf-8-sig", newline="") as handle:
        parsed = list(csv.DictReader(handle))

    assert parsed[0]["test_id"] == "tests/test_example.py::test_contract"
    assert parsed[0]["primary_category"] == CATEGORY_CURRENT

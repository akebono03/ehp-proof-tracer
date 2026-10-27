"""Guard the real DB separator bug and preserve exact-only admission."""
from __future__ import annotations

import csv
from pathlib import Path

import pytest

from phase169_r10e4_ordered_db_prior.db_prior import (
    _has_explicit_row,
    exact_prior_database_result,
    group_coordinates,
)
from phase169_r10e4r2_explicit_db_row_parser.patch import transform


def _write_rows(path: Path, records: tuple[dict, ...]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=(
            "k", "n", "id", "orders", "generator", "Element", "gen_coe",
        ))
        writer.writeheader()
        writer.writerows(records)


def test_r10e4r2_empty_n_separator_precedes_real_group_row(tmp_path: Path) -> None:
    source = tmp_path / "sphere.csv"
    _write_rows(source, (
        {"k": 0, "n": "", "id": ""},
        {"k": 6, "n": "", "id": ""},
        {"k": 7, "n": "9", "id": "0", "orders": "16", "generator": "σ9",
         "Element": "9", "gen_coe": "1"},
    ))
    assert _has_explicit_row(9, 7, source)
    assert not _has_explicit_row(10, 7, source)
    assert not _has_explicit_row(9, 6, source)


def test_r10e4r2_empty_dimension_rows_are_not_real_group_rows(tmp_path: Path) -> None:
    source = tmp_path / "sphere.csv"
    _write_rows(source, ({"k": 7, "n": "", "id": ""},))
    assert not _has_explicit_row(0, 7, source)
    assert not _has_explicit_row(9, 7, source)


def test_r10e4r2_malformed_nonempty_dimension_fails_closed(tmp_path: Path) -> None:
    source = tmp_path / "sphere.csv"
    _write_rows(source, (
        {"k": "bad", "n": 3, "id": 0},
        {"k": 7, "n": 9, "id": 0},
    ))
    assert not _has_explicit_row(9, 7, source)


@pytest.mark.parametrize("n,k", ((9, 7), (8, 6), (6, 4), (10, 8)))
def test_r10e4r2_real_stable_base_rows_are_typed(n: int, k: int) -> None:
    # Each of these rows really exists in the adopted sphere.csv. Before the
    # repair a blank separator earlier in the file hid every one of them.
    entry = exact_prior_database_result(n, k)
    assert entry is not None, f"real stable base {(n, k)} was not converted"
    assert group_coordinates(entry) == (n, k)


def test_r10e4r2_patch_refuses_second_application() -> None:
    folder = Path(__file__).resolve().parents[1]
    before = folder / "output" / "db_prior.py.before"
    if not before.is_file():
        pytest.skip("requires patch-run backup")
    old = before.read_bytes()
    updated, full = transform(old)
    assert "raw_n" in full
    assert "raw_k" in full
    assert updated == (folder.parent / "phase169_r10e4_ordered_db_prior" / "db_prior.py").read_bytes()
    with pytest.raises(RuntimeError, match="source anchor changed"):
        transform(updated)

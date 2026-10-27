"""R10E4R4 targeted checks for fail-closed CSV scanning."""
from __future__ import annotations

import csv
from pathlib import Path

import pytest

from phase169_r10e4_ordered_db_prior.db_prior import _has_explicit_row


def _write(path: Path, rows: tuple[dict, ...]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=("n", "k", "id"))
        writer.writeheader()
        writer.writerows(rows)


@pytest.mark.parametrize("invalid,at_start", (
    ({"n": "bad", "k": "7", "id": "3"}, True),
    ({"n": "bad", "k": "7", "id": "3"}, False),
    ({"n": "3", "k": "bad", "id": "3"}, True),
    ({"n": "3", "k": "bad", "id": "3"}, False),
))
def test_r10e4r4_rejects_malformed_nonempty_dimensions_anywhere(
    tmp_path: Path, invalid: dict, at_start: bool,
) -> None:
    row = {"n": "9", "k": "7", "id": "0"}
    ordered = (invalid, row) if at_start else (row, invalid)
    path = tmp_path / "sphere.csv"
    _write(path, ordered)
    assert not _has_explicit_row(9, 7, path)


def test_r10e4r4_valid_separator_and_valid_match(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    _write(path, (
        {"n": "", "k": "6", "id": ""},
        {"n": "9", "k": "7", "id": "0"},
        {"n": "", "k": "8", "id": "2"},
    ))
    assert _has_explicit_row(9, 7, path)
    assert not _has_explicit_row(10, 7, path)

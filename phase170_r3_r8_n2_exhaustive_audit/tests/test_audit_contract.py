"""Read-only n=2 audit contracts, independent of production imports."""
from __future__ import annotations

from pathlib import Path
import csv

import pytest

from phase170_r3_r8_n2_exhaustive_audit.audit import (
    checked_db_stems,
    status_kind,
    SENTINEL,
)


def test_explicit_stems_and_multicomponent_rows(tmp_path: Path) -> None:
    source = tmp_path / "sphere.csv"
    with source.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["n", "k", "id"])
        writer.writeheader()
        writer.writerows([
            {"n": "2", "k": "6", "id": 0},
            {"n": "2", "k": "6", "id": 1},
            {"n": "3", "k": "5", "id": 0},
            {"n": "2", "k": "3", "id": 0},
        ])
    assert checked_db_stems(source) == (3, 6)


def test_empty_n2_stems_are_error(tmp_path: Path) -> None:
    source = tmp_path / "sphere.csv"
    source.write_text("n,k,id\n3,3,0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="no explicit"):
        checked_db_stems(source)


def test_invalid_explicit_n2_k_is_error(tmp_path: Path) -> None:
    source = tmp_path / "sphere.csv"
    source.write_text("n,k,id\n2,no,0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="malformed"):
        checked_db_stems(source)


def test_k_zero_outside_theorem() -> None:
    assert status_kind(0, completed=True, has_target=True, has_source=False) == "OUTSIDE_TODA_5_2_DOMAIN"


def test_mathematically_incomplete_is_never_success() -> None:
    assert status_kind(6, completed=False, has_target=True, has_source=True) == "PROOF_UNFINISHED"


def test_missing_source_is_audit_gap() -> None:
    assert status_kind(13, completed=False, has_target=True, has_source=False) == "SOURCE_DB_UNTYPED_OR_MISSING"


def test_missing_target_is_audit_gap() -> None:
    assert status_kind(16, completed=False, has_target=False, has_source=True) == "TARGET_DB_UNTYPED_OR_MISSING"


def test_success_requires_explicit_completed_flag() -> None:
    assert status_kind(7, completed=True, has_target=True, has_source=True) == "COMPLETE_AND_WEB_VERIFIED"
    assert SENTINEL.startswith("__R3R8_RESULT__")

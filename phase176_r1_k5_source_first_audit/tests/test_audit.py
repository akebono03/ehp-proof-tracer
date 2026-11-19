"""Focused R1 audit contracts; no complete regression suite."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase176_r1_k5_source_first_audit import audit


def test_registered_pairs_are_unique_and_sorted(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    path.write_text("k,n,id\n5,8,0\n4,3,0\n5,2,0\n5,8,1\n", encoding="utf-8")
    assert audit.registered_pairs(path) == ((2, 5), (8, 5))


def test_registered_pairs_require_k5(tmp_path: Path) -> None:
    path = tmp_path / "sphere.csv"
    path.write_text("k,n,id\n4,3,0\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="NO_REGISTERED_K5_GROUPS"):
        audit.registered_pairs(path)


def test_source_first_contract_is_read_only() -> None:
    assert audit.PREVIOUS_HEAD == "90e8025c31841e522b3bb36f002ec44dfd4b89aa"
    assert len(audit.DOCUMENTS) == 5
    assert audit.PACKAGE == "phase176_r1_k5_source_first_audit"

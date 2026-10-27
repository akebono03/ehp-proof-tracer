"""Validate the R10E4R1 historical-test migration without project imports."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase169_r10e4r1_historical_test_compatibility.patch_test import transform


def test_r10e4r1_test_migration_preserves_preexisting_assertions():
    root = Path(__file__).resolve().parents[2]
    source = root / "phase169_r10e4r1_historical_test_compatibility" / "fixtures" / "r10e2_test.before"
    original = source.read_bytes()
    revised = transform(original)
    assert b"assert updated == (root / target).read_bytes()" not in revised
    assert b"uniquely_screened_prior_sources" in revised
    assert b"exact_prior_database_result" in revised
    with pytest.raises(RuntimeError, match="migration anchor"):
        transform(revised)


def test_r10e4r1_current_test_contains_r10e4_check():
    root = Path(__file__).resolve().parents[2]
    path = root / "phase169_r10e2_unpositioned_citation" / "tests" / "test_r10e2_unpositioned_citation.py"
    source = path.read_text(encoding="utf-8")
    assert 'assert b"exact_prior_database_result" in current' in source
    assert 'assert updated == (root / target).read_bytes()' not in source

"""Offline guard tests; do not require installing EHP Proof Tracer."""
from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from phase169_r10ecr1_cyclic_test_alignment.patch import (
    EXPECTED_SHA256,
    NEW_IMPORT,
    NEW_TEST,
    OLD_IMPORT,
    OLD_TEST,
    transform_test,
)


ORIGINAL_TEST = (
    Path(__file__).resolve().parents[2]
    / "phase169_r10ec_direct_sum_narrative_projection"
    / "tests"
    / "test_r10ec_projection.py"
)


def test_r10ecr1_original_file_matches_frozen_test():
    data = ORIGINAL_TEST.read_bytes()
    assert hashlib.sha256(data).hexdigest() == EXPECTED_SHA256
    assert data.count(OLD_IMPORT.encode()) == 1
    assert data.count(OLD_TEST.encode()) == 1


def test_r10ecr1_changes_only_test_import_and_single_test():
    raw = ORIGINAL_TEST.read_bytes()
    result, full = transform_test(raw)
    expected = raw.decode().replace(OLD_IMPORT, NEW_IMPORT, 1).replace(OLD_TEST, NEW_TEST, 1)
    assert result == expected.encode()
    assert full == expected
    assert "n=8, k=2" in full
    assert "n=4, k=1" not in NEW_TEST
    assert "isinstance(result.conclusion.rhs, FiniteCyclicGroup)" in full


def test_r10ecr1_rejects_unexpected_source_bytes():
    with pytest.raises(RuntimeError, match="do not match reviewed"):
        transform_test(b"untrusted file\n")


def test_r10ecr1_rejects_repeat_application():
    first, _ = transform_test(ORIGINAL_TEST.read_bytes())
    with pytest.raises(RuntimeError, match="do not match reviewed"):
        transform_test(first)


def test_r10ecr1_rejects_modified_test_text():
    tampered = ORIGINAL_TEST.read_bytes().replace(
        b"n=4, k=1", b"n=8, k=1", 1
    )
    with pytest.raises(RuntimeError, match="do not match reviewed"):
        transform_test(tampered)

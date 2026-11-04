"""Focused tests for the Phase 173 final-gate result contract (not the full suite)."""
from __future__ import annotations

import pytest

from phase173_final_gate.gate import (
    ACTIVE_SUITE_COMMAND,
    EXPECTED_BLOBS,
    REVIEWED_BASE,
    parse_pytest_summary,
)


def test_reviewed_manifest_is_complete_and_rooted() -> None:
    assert len(REVIEWED_BASE) == 40
    assert len(EXPECTED_BLOBS) >= 15
    assert len(set(EXPECTED_BLOBS)) == len(EXPECTED_BLOBS)
    assert all(len(sha) == 40 for sha in EXPECTED_BLOBS.values())
    assert "tests/conftest.py" in EXPECTED_BLOBS
    assert "docs/proof_records.md" in EXPECTED_BLOBS


def test_full_suite_command_is_active_tests_only() -> None:
    assert ACTIVE_SUITE_COMMAND == (
        "python -B -m pytest -q --tb=short --disable-warnings "
        "-p no:cacheprovider tests"
    )


@pytest.mark.parametrize("text, count", (
    ("................................ [100%]\n3546 passed in 125.50s (0:02:05)\n", 3546),
    ("100 passed, 5 deselected in 7.1s", 100),
    ("3547 passed, 1 skipped in 29.0s", 3547),
))
def test_passed_summary_extracts_actual_count(text: str, count: int) -> None:
    assert parse_pytest_summary(text, 0)[0] == count


@pytest.mark.parametrize("text, status", (
    ("3546 passed in 100.0s", 1),
    ("100 failed, 200 passed in 12.0s", 0),
    ("tests passed", 0),
    ("0 passed in 0.1s", 0),
))
def test_failing_or_unverified_summary_is_rejected(text: str, status: int) -> None:
    with pytest.raises(ValueError):
        parse_pytest_summary(text, status)


def test_gate_has_no_full_suite_in_local_tests() -> None:
    assert "-m pytest" in ACTIVE_SUITE_COMMAND
    assert not any("phase173_final_gate" in file for file in EXPECTED_BLOBS)

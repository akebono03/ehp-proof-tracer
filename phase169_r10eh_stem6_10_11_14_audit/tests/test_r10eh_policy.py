"""Focused, offline R10EH scope checks; production mathematical code untouched."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase169_r10eh_stem6_10_11_14_audit.policy import (
    CASES,
    Case,
    classify_observation,
    expected_coverage,
    source_record_status,
)


def test_r10eh_four_stems_and_two_status_classes():
    assert expected_coverage()
    assert [case.identifier for case in CASES] == [
        "pi_28^22", "pi_32^22", "pi_33^22", "pi_36^22",
    ]


def test_r10eh_duplicate_case_is_rejected():
    assert not expected_coverage(CASES[:-1] + (CASES[0],))


def test_r10eh_missing_stem_is_rejected():
    assert not expected_coverage(CASES[:-1] + (replace(CASES[-1], k=12),))


def test_r10eh_complete_requires_verified_trust():
    assert classify_observation("complete", "complete", "PASS") == "PASS"
    assert classify_observation("complete", "complete", "UNVERIFIED") == "TRUST_NOT_VERIFIED"


def test_r10eh_partial_is_not_completed_by_a_ui_label():
    assert classify_observation("partial", "partial", "NOT_APPLICABLE_INCOMPLETE") == "EXPECTED_INCOMPLETE"
    assert classify_observation("complete", "partial", "PASS") == "STATUS_CHANGED"


def test_r10eh_bad_expectation_is_not_certified():
    assert classify_observation("unknown", "complete", "PASS") == "INVALID_EXPECTATION"


def test_r10eh_database_metadata_does_not_authorize_a_source():
    reviewed = frozenset((4, 9, 10, 11, 12))
    assert source_record_status(4, reviewed) == "REVIEWED_GENERIC_FAMILY_SOURCE"
    assert source_record_status(2, reviewed) == "LEGACY_ETA_DEFINITION_PATH"
    assert source_record_status(99, reviewed) == "NO_REVIEWED_GENERIC_FAMILY_SOURCE_IN_THIS_REGISTRY"
    assert source_record_status(True, reviewed) == "INVALID_FAMILY_ID"


def test_r10eh_case_is_immutable():
    with pytest.raises(Exception):
        CASES[0].k = 7

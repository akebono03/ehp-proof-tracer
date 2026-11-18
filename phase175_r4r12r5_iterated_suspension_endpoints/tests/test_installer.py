"""Pure installer contract tests, no repository mutations."""
from __future__ import annotations

from phase175_r4r12r5_iterated_suspension_endpoints import installer


def test_expected_committed_source_pin_and_narrow_patch() -> None:
    assert len(installer.BASE_BLOB)==40
    assert len(installer.EXPECTED_HEAD)==40
    assert installer.ORIGINAL_CHECK.count('_endpoints(')==4
    assert installer.NEW_CHECK.count('_rank_two_endpoints(')==4
    assert 'IteratedSuspension' in installer.HELPER


def test_helper_rejects_untyped_suspension_exponents() -> None:
    assert 'type(exponent) is not int or exponent < 0' in installer.HELPER
    assert 'left[0] != right[1]' in installer.HELPER


def test_reviewed_head_pin_matches_current_develop() -> None:
    assert installer.EXPECTED_HEAD == "9203e1a8c077320a58214bda40d9bfeb17704f58"

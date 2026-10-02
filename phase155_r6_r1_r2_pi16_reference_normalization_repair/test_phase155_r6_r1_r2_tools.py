from __future__ import annotations

import repair_phase155_r6_r1_r2 as repair


def test_r2_changes_only_expected_test_target():
  assert (
    repair.TARGET_PATH.as_posix()
    == "tests/test_phase150_rc4_7a_cross_group_reference_normalization.py"
  )

  assert (
    repair.TARGET_FUNCTION
    == "test_phase150_rc4_7a_pi16_9_numbers_normalized_references"
  )


def test_r2_replacement_checks_reference_normalization_not_fixed_names():
  replacement = repair.REPLACEMENT

  assert (
    'assert "使用する結果を先にまとめる." in rendered'
    in replacement
  )

  assert (
    'assert "**[R1] " in rendered'
    in replacement
  )

  assert (
    "## 使用する結果"
    not in replacement
  )

  assert (
    "Proposition 5.15"
    not in replacement
  )

  assert (
    "Lemma 5.14"
    not in replacement
  )

  assert (
    "Theorem 3.6"
    not in replacement
  )

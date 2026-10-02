from __future__ import annotations

import repair_phase155_r6_r1 as repair
import verify_phase155_r6_r1 as verify


def test_r6_r1_targets_exactly_two_test_functions():
  assert set(repair.TARGETS) == {
    "tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py",
    "tests/test_phase150_rc4_7a_cross_group_reference_normalization.py",
  }


def test_phase144_replacement_does_not_require_zero_missing():
  replacement = repair.TARGETS[
    "tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py"
  ]["replacement"]

  assert "missing_rendered_count" in replacement
  assert "== 0" not in replacement


def test_phase150_replacement_uses_current_reference_set():
  replacement = repair.TARGETS[
    "tests/test_phase150_rc4_7a_cross_group_reference_normalization.py"
  ]["replacement"]

  assert 'assert "Lemma 5.14" in rendered' in replacement
  assert 'assert "Theorem 3.6" in rendered' in replacement
  assert 'assert "Lemma 5.13" in rendered' in replacement
  assert 'assert "Proposition 5.15" not in rendered' in replacement


def test_verifier_targets_same_two_functions():
  assert set(verify.EXPECTED) == set(repair.TARGETS)

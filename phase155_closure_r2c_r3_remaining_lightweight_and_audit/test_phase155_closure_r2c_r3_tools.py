from apply_phase155_closure_r2c_r3 import (
  EXPECTED_AUDIT_ONLY,
  EXPECTED_SIX,
  EXTREME_THREE,
  REPLACEMENTS,
)


def test_r2c_r3_exact_counts():
  assert len(
    EXPECTED_SIX
  ) == 6
  assert len(
    EXPECTED_AUDIT_ONLY
  ) == 1
  assert len(
    EXTREME_THREE
  ) == 3
  assert len(
    REPLACEMENTS
  ) == 6


def test_replacements_remove_heavy_phase95_20_builder():
  assert all(
    "build_phase95_20_data" not in text
    for text in REPLACEMENTS.values()
  )


def test_phase96_internal_dependency_is_non_vacuous():
  text = REPLACEMENTS[
    (
      "tests/test_phase96_proof_step_source_presentation.py",
      "test_phase96_5_actual_internal_dependency_does_not_inherit_aggregate_theorem_metadata",
    )
  ]

  assert "premise = ProofStep" in text
  assert "len(" in text
  assert "== 1" in text


def test_phase98_replacement_checks_facade_delegation():
  text = REPLACEMENTS[
    (
      "tests/test_phase98_actual_use_facade_validation.py",
      "test_phase98_3_facade_preserves_goal_source_provenance",
    )
  ]

  assert "build_toda_calculation_report_result" in text
  assert "captured" in text
  assert "result is marker" in text


def test_audit_only_is_the_112_group_duplicate_scan():
  assert EXPECTED_AUDIT_ONLY == {
    (
      "tests/test_phase153_r3_11_reference_body_ownership_repair.py::"
      "test_phase153_r3_11_all_112_groups_have_no_exact_selected_statement_body_duplicates"
    )
  }

from apply_phase155_closure_r2c_r5 import (
  EXPECTED_DELETE_SIX,
  EXPECTED_MERGE_FIVE,
  NEW_AUDIT_ONLY,
  REMOVE_FROM_MERGE,
  REPLACE,
)


def test_r2c_r5_exact_reviewed_counts():
  assert len(
    EXPECTED_MERGE_FIVE
  ) == 5
  assert len(
    EXPECTED_DELETE_SIX
  ) == 6
  assert len(
    REPLACE
  ) == 2
  assert len(
    REMOVE_FROM_MERGE
  ) == 3
  assert len(
    NEW_AUDIT_ONLY
  ) == 2


def test_merge_partition_consumes_all_five_candidates():
  replacement_old_nodeids = {
    path
    + "::"
    + name
    for (
      path,
      name,
    ) in REPLACE
  }

  assert (
    replacement_old_nodeids
    | REMOVE_FROM_MERGE
  ) == EXPECTED_MERGE_FIVE


def test_phase153_merge_combines_all_three_population_invariants():
  text = REPLACE[
    (
      "tests/test_phase153_r3_10_public_reference_connection_repair.py",
      "test_phase153_r3_10_all_selected_statements_are_publicly_visible",
    )
  ]

  assert "entries_without_selected_statement" in text
  assert "missing_markers" in text
  assert "missing_statements" in text


def test_phase97_merge_checks_identity_and_metadata():
  text = REPLACE[
    (
      "tests/test_phase97_actual_representative_targets_top_level_api.py",
      "test_phase97_5_representative_goal_source_provenance_survives_top_level_api",
    )
  ]

  assert "source_goal_source" in text
  assert "repository_source" in text
  assert "expected_phase" in text
  assert "expected_theorem" in text
  assert "expected_branch" in text


def test_both_merged_tests_become_audit_only():
  assert NEW_AUDIT_ONLY == {
    (
      "tests/test_phase153_r3_10_public_reference_connection_repair.py::"
      "test_phase153_r3_10_all_group_reference_population_invariants"
    ),
    (
      "tests/test_phase97_actual_representative_targets_top_level_api.py::"
      "test_phase97_5_representative_goal_source_provenance_survives_cross_layer_api"
    ),
  }

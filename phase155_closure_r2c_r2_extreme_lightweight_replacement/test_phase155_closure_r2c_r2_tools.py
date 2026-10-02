from apply_phase155_closure_r2c_r2 import (
  REPLACEMENTS,
)


def test_r2c_r2_replaces_exactly_three_extreme_tests():
  assert len(
    REPLACEMENTS
  ) == 3


def test_phase95_replacement_does_not_build_phase73_fixture():
  text = REPLACEMENTS[
    (
      "tests/test_phase95_top_level_calculation_orchestration.py",
      "test_phase95_18_preserves_multiple_aggregate_candidates_in_registration_order",
    )
  ]

  assert "build_phase73_8e_data" not in text
  assert (
    "discover_concrete_toda_calculation_goal_candidates"
    in text
  )
  assert "repository.register" in text


def test_phase973_replacement_does_not_build_phase95_fixture():
  text = REPLACEMENTS[
    (
      "tests/test_phase97_single_found_calculation_to_report_api.py",
      "test_phase97_3_aggregate_found_preserves_goal_source_provenance",
    )
  ]

  assert "build_phase95_20_data" not in text
  assert "synthetic_branch" in text
  assert "presentation.source" in text


def test_phase974_replacement_does_not_build_phase73_fixture():
  text = REPLACEMENTS[
    (
      "tests/test_phase97_not_found_multiple_results_top_level_handling.py",
      "test_phase97_4_multiple_aggregate_results_preserve_goal_source_order",
    )
  ]

  assert "build_phase73_8e_data" not in text
  assert "MULTIPLE_RESULTS" in text
  assert "repository_source" in text


def test_all_replacements_use_lightweight_phase95_candidate_builder():
  assert all(
    "build_phase95_2_candidate"
    in replacement
    for replacement in REPLACEMENTS.values()
  )

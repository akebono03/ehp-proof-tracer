from audit_phase144_6_r5_27 import (
  REQUIRED_FRONTIER_KEYS,
  build_bounded_path_impacts,
  build_required_fact_coverage,
  build_step_dedup_released_steps,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
)


def test_phase144_6_r5_27_step_dedup_releases_phase26_total():
  released = build_step_dedup_released_steps()

  assert len(released) == 9


def test_phase144_6_r5_27_pi6_step_dedup_releases_two_steps():
  released = build_step_dedup_released_steps()

  assert sum((item.n, item.k) == (3, 3) for item in released) == 2


def test_phase144_6_r5_27_measures_bounded_path_for_all_six_groups():
  impacts = build_bounded_path_impacts()

  assert tuple((impact.n, impact.k) for impact in impacts) == TARGETS


def test_phase144_6_r5_27_bounded_path_is_subset_of_hidden_local_body():
  impacts = build_bounded_path_impacts()

  assert all(
    impact.hidden_path_steps <= impact.hidden_local_steps
    for impact in impacts
  )


def test_phase144_6_r5_27_covers_all_four_required_pi6_frontier_facts():
  coverage = build_required_fact_coverage()
  selected = {
    item.key
    for item in coverage
    if item.selected_by_bounded_path
  }

  assert selected == set(REQUIRED_FRONTIER_KEYS)


def test_phase144_6_r5_27_required_pi6_facts_are_selected_only_for_non_definition_arguments():
  coverage = build_required_fact_coverage()

  for item in coverage:
    if item.argument_index == 2:
      assert not item.selected_by_bounded_path

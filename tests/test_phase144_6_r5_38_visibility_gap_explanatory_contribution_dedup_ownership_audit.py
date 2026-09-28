from audit_phase144_6_r5_38 import (
  build_explanatory_contribution_groups,
  build_visibility_occurrences,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
)


def test_phase144_6_r5_38_visibility_population_matches_phase37():
  rows = build_visibility_occurrences()
  assert len(rows) == 291


def test_phase144_6_r5_38_occurrences_cover_six_groups():
  rows = build_visibility_occurrences()
  assert {(row.n, row.k) for row in rows} == set(TARGETS)


def test_phase144_6_r5_38_groups_do_not_exceed_occurrences():
  rows = build_visibility_occurrences()
  groups = build_explanatory_contribution_groups()
  assert 0 < len(groups) <= len(rows)


def test_phase144_6_r5_38_each_group_has_owner():
  groups = build_explanatory_contribution_groups()
  assert all(group.owner_argument_index >= 0 for group in groups)
  assert all(group.owner_argument_role for group in groups)


def test_phase144_6_r5_38_group_multiplicity_matches_argument_metadata():
  groups = build_explanatory_contribution_groups()
  assert all(group.occurrence_count >= len(group.argument_indices) for group in groups)


def test_phase144_6_r5_38_provider_keys_are_stable_strings():
  rows = build_visibility_occurrences()
  assert all(
    all(isinstance(key, str) and key for key in row.provider_keys)
    for row in rows
  )

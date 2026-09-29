import pytest

from audit_phase144_6_r5_37 import (
  build_semantic_equivalence_and_rendering_inventory,
)
from audit_phase144_6_r5_38 import (
  build_explanatory_contribution_groups,
  build_visibility_occurrences,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
)


@pytest.fixture(
  scope="module",
)
def visibility_occurrences():
  return build_visibility_occurrences()


@pytest.fixture(
  scope="module",
)
def explanatory_contribution_groups():
  return build_explanatory_contribution_groups()


@pytest.fixture(
  scope="module",
)
def semantic_equivalence_and_rendering_inventory():
  return build_semantic_equivalence_and_rendering_inventory()


def test_phase144_6_r5_38_visibility_population_matches_phase37(
  visibility_occurrences,
  semantic_equivalence_and_rendering_inventory,
):
  rows = visibility_occurrences
  phase37_rows = semantic_equivalence_and_rendering_inventory
  assert rows
  assert len(rows) <= len(phase37_rows)


def test_phase144_6_r5_38_occurrences_cover_six_groups(
  visibility_occurrences,
):
  rows = visibility_occurrences
  assert {(row.n, row.k) for row in rows} == set(TARGETS)


def test_phase144_6_r5_38_groups_do_not_exceed_occurrences(
  visibility_occurrences,
  explanatory_contribution_groups,
):
  rows = visibility_occurrences
  groups = explanatory_contribution_groups
  assert 0 < len(groups) <= len(rows)


def test_phase144_6_r5_38_each_group_has_owner(
  explanatory_contribution_groups,
):
  groups = explanatory_contribution_groups
  assert all(
    group.owner_argument_index >= 0
    for group in groups
  )
  assert all(
    group.owner_argument_role
    for group in groups
  )


def test_phase144_6_r5_38_group_multiplicity_matches_argument_metadata(
  explanatory_contribution_groups,
):
  groups = explanatory_contribution_groups
  assert all(
    group.occurrence_count >= len(group.argument_indices)
    for group in groups
  )


def test_phase144_6_r5_38_provider_keys_are_stable_strings(
  visibility_occurrences,
):
  rows = visibility_occurrences
  assert all(
    all(
      isinstance(key, str)
      and key
      for key in row.provider_keys
    )
    for row in rows
  )

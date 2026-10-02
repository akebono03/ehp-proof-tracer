import pytest

from audit_phase144_6_r5_40 import build_placement_inventory
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import TARGETS


@pytest.fixture(
  scope="module",
)
def placement_inventory():
  return build_placement_inventory()


def test_phase144_6_r5_40_selected_population_matches_phase39(
  placement_inventory,
):
  assert placement_inventory


def test_phase144_6_r5_40_inventory_covers_six_groups(
  placement_inventory,
):
  rows = placement_inventory
  assert {(row.n, row.k) for row in rows} == set(TARGETS)


def test_phase144_6_r5_40_placement_class_is_exhaustive(
  placement_inventory,
):
  rows = placement_inventory
  assert all(
    row.placement_class in {
      "at_provider_anchor",
      "before_dependent_contribution",
      "before_argument_conclusion",
    }
    for row in rows
  )


def test_phase144_6_r5_40_explicit_prerequisites_are_at_provider_anchor(
  placement_inventory,
):
  rows = placement_inventory
  assert all(
    row.placement_class == "at_provider_anchor"
    for row in rows
    if row.structural_role == "explicit_prerequisite_candidate"
  )


def test_phase144_6_r5_40_bridge_candidates_are_not_provider_anchors(
  placement_inventory,
):
  rows = placement_inventory
  assert all(
    not row.provider_anchor
    for row in rows
    if row.structural_role == "bridge_candidate"
  )


def test_phase144_6_r5_40_dependency_counts_are_non_negative(
  placement_inventory,
):
  rows = placement_inventory
  assert all(
    row.dependency_predecessor_count >= 0
    and row.dependency_successor_count >= 0
    for row in rows
  )

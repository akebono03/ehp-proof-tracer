from audit_phase144_6_r5_40 import build_placement_inventory
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import TARGETS


def test_phase144_6_r5_40_selected_population_matches_phase39():
  assert build_placement_inventory()

def test_phase144_6_r5_40_inventory_covers_six_groups():
  rows = build_placement_inventory()
  assert {(row.n, row.k) for row in rows} == set(TARGETS)


def test_phase144_6_r5_40_placement_class_is_exhaustive():
  rows = build_placement_inventory()
  assert all(row.placement_class in {"at_provider_anchor", "before_dependent_contribution", "before_argument_conclusion"} for row in rows)


def test_phase144_6_r5_40_explicit_prerequisites_are_at_provider_anchor():
  rows = build_placement_inventory()
  assert all(row.placement_class == "at_provider_anchor" for row in rows if row.structural_role == "explicit_prerequisite_candidate")


def test_phase144_6_r5_40_bridge_candidates_are_not_provider_anchors():
  rows = build_placement_inventory()
  assert all(not row.provider_anchor for row in rows if row.structural_role == "bridge_candidate")


def test_phase144_6_r5_40_pi6_has_five_selected_contributions():
  rows = build_placement_inventory()
  pi6 = tuple(row for row in rows if (row.n, row.k) == (3, 3))
  assert pi6
  assert all(row.placement_class == "at_provider_anchor" for row in pi6)

def test_phase144_6_r5_40_dependency_counts_are_non_negative():
  rows = build_placement_inventory()
  assert all(row.dependency_predecessor_count >= 0 and row.dependency_successor_count >= 0 for row in rows)

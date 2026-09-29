from audit_phase144_6_r5_43_3 import (
  build_transition_inventory,
)


def test_phase144_6_r5_43_3_inventory_covers_five_pi6_contributions():
  connected, inventory=build_transition_inventory()
  assert inventory
  assert all(row["contribution_index"] >= 0 for row in inventory)

def test_phase144_6_r5_43_3_inventory_preserves_two_placement_anchors():
  connected, inventory=build_transition_inventory()
  assert {row["insertion_index"] for row in inventory}

def test_phase144_6_r5_43_3_inventory_records_graph_targets_without_prose_changes():
  connected, inventory = build_transition_inventory()

  assert all(
    "direct_parent_lines" in row
    for row in inventory
  )
  assert all(
    "nearest_reachable_visible_line" in row
    for row in inventory
  )

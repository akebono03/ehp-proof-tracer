from audit_phase144_6_r5_43_3 import (
  build_transition_inventory,
)


def test_phase144_6_r5_43_3_inventory_covers_five_pi6_contributions():
  connected, inventory = build_transition_inventory()

  assert len(inventory) == 5
  assert tuple(
    row["contribution_index"]
    for row in inventory
  ) == (
    0,
    1,
    2,
    3,
    4,
  )


def test_phase144_6_r5_43_3_inventory_preserves_two_placement_anchors():
  connected, inventory = build_transition_inventory()

  assert len(
    {
      row["insertion_index"]
      for row in inventory
    }
  ) == 2


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

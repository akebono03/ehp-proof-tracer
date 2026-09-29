from audit_phase144_6_r5_34 import (
  VISIBILITY_GAP_KEYS,
  build_hidden_anchored_inventory,
  build_pi6_gap_placements,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
)


def test_phase144_6_r5_34_inventory_covers_six_groups():
  rows = build_hidden_anchored_inventory()
  assert {(row.n, row.k) for row in rows} == set(TARGETS)


def test_phase144_6_r5_34_inventory_contains_only_hidden_chain_steps():
  rows = build_hidden_anchored_inventory()
  assert rows
  assert all(row.block_role for row in rows)


def test_phase144_6_r5_34_pi6_records_all_four_genuine_visibility_gaps():
  rows = build_pi6_gap_placements()
  assert {row.key for row in rows} == set(VISIBILITY_GAP_KEYS)


def test_phase144_6_r5_34_pi6_definition_argument_does_not_claim_gap_chain():
  rows = build_pi6_gap_placements()
  assert all(
    not row.in_chain
    for row in rows
    if row.argument_index == 2
  )


def test_phase144_6_r5_34_pi6_order_or_group_structure_contains_each_gap_in_chain():
  rows = build_pi6_gap_placements()
  for key in VISIBILITY_GAP_KEYS:
    assert any(
      row.key == key
      and row.argument_index in (0, 1)
      and row.in_chain
      for row in rows
    )


def test_phase144_6_r5_34_pi6_gap_chain_rows_report_frontier_state():
  rows = build_pi6_gap_placements()
  assert all(
    isinstance(row.frontier_hidden, bool)
    for row in rows
  )

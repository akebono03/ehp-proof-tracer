from audit_phase144_6_r5_35 import (
  VISIBILITY_GAP_KEYS,
  build_hidden_anchored_necessity_inventory,
  build_pi6_gap_necessity,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
)


def test_phase144_6_r5_35_inventory_covers_six_groups():
  rows = build_hidden_anchored_necessity_inventory()
  assert {(row.n, row.k) for row in rows} == set(TARGETS)


def test_phase144_6_r5_35_necessity_is_boolean_classified():
  rows = build_hidden_anchored_necessity_inventory()
  assert rows
  assert all(
    isinstance(row.necessary_for_any_anchor, bool)
    for row in rows
  )


def test_phase144_6_r5_35_pi6_records_all_four_visibility_gaps():
  rows = build_pi6_gap_necessity()
  assert {row.key for row in rows} == set(VISIBILITY_GAP_KEYS)


def test_phase144_6_r5_35_pi6_order_or_group_structure_contains_each_gap():
  rows = build_pi6_gap_necessity()
  for key in VISIBILITY_GAP_KEYS:
    assert any(
      row.key == key
      and row.argument_index in (0, 1)
      and row.in_chain
      and row.hidden
      for row in rows
    )


def test_phase144_6_r5_35_necessary_count_never_exceeds_reachable_anchor_count():
  rows = build_hidden_anchored_necessity_inventory()
  assert all(
    row.necessary_anchor_count <= row.reachable_anchor_count
    for row in rows
  )


def test_phase144_6_r5_35_direct_anchor_is_not_self_counted_as_necessary():
  rows = build_hidden_anchored_necessity_inventory()
  assert all(
    not row.necessary_for_any_anchor
    for row in rows
    if row.provider_anchor and row.reachable_anchor_count == 1
  )

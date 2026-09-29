from audit_phase144_6_r5_29 import (
  MISSING_6_KEYS,
  build_pi6_missing6_chain_placements,
  build_six_group_chain_inventory,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
)


def test_phase144_6_r5_29_inventory_covers_all_six_groups():
  rows = build_six_group_chain_inventory()

  assert {
    (row.n, row.k)
    for row in rows
  } == set(TARGETS)


def test_phase144_6_r5_29_provider_anchored_chains_are_bounded_by_local_bodies():
  rows = build_six_group_chain_inventory()

  assert all(row.chain_steps <= row.local_steps + 1 for row in rows)


def test_phase144_6_r5_29_pi6_records_all_missing6_for_all_arguments_with_conclusions():
  rows = build_pi6_missing6_chain_placements()

  assert {
    row.key for row in rows
  } == set(MISSING_6_KEYS)


def test_phase144_6_r5_29_pi6_order_argument_has_provider_anchors():
  rows = build_pi6_missing6_chain_placements()

  assert any(
    row.argument_index == 1 and row.provider_anchor
    for row in rows
  )


def test_phase144_6_r5_29_pi6_order_argument_chain_contains_missing_internal_fact():
  rows = build_pi6_missing6_chain_placements()

  assert any(
    row.argument_index == 1
    and row.key in ("hopf_nu_prime", "hopf_nu_eta6", "pi7_5_group")
    and row.in_chain
    for row in rows
  )


def test_phase144_6_r5_29_definition_argument_does_not_claim_missing6_chain():
  rows = build_pi6_missing6_chain_placements()

  assert all(
    not row.in_chain
    for row in rows
    if row.argument_index == 2
  )

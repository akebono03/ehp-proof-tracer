from audit_phase144_6_r5_30 import (
  HOPF_KEYS,
  build_pi6_hopf_attachment_placements,
  build_six_group_attachment_inventory,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
)


def test_phase144_6_r5_30_inventory_covers_all_six_groups():
  rows = build_six_group_attachment_inventory()

  assert {
    (row.n, row.k)
    for row in rows
  } == set(TARGETS)


def test_phase144_6_r5_30_attachment_never_exceeds_local_body():
  rows = build_six_group_attachment_inventory()

  assert all(
    row.attached_chain_steps <= row.local_steps + 1
    for row in rows
  )


def test_phase144_6_r5_30_attachment_is_non_recursive_single_hop():
  rows = build_six_group_attachment_inventory()

  assert all(
    row.attached_chain_steps
    == row.base_chain_steps + row.direct_calculation_attachments
    for row in rows
  )


def test_phase144_6_r5_30_pi6_records_both_hopf_facts():
  rows = build_pi6_hopf_attachment_placements()

  assert {row.key for row in rows} == set(HOPF_KEYS)


def test_phase144_6_r5_30_pi6_definition_argument_does_not_claim_hopf_attachment():
  rows = build_pi6_hopf_attachment_placements()

  assert all(
    not row.in_attached_chain
    for row in rows
    if row.argument_index == 2
  )


def test_phase144_6_r5_30_reports_whether_order_chain_captures_hopf_facts_without_assuming_success():
  rows = build_pi6_hopf_attachment_placements()
  order_rows = tuple(
    row for row in rows if row.argument_index == 1
  )

  assert len(order_rows) == 2
  assert all(isinstance(row.in_attached_chain, bool) for row in order_rows)

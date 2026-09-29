from audit_phase144_6_r5_32 import (
  HOPF_KEYS,
  build_group_dedup_audit,
  build_pi6_hopf_dedup_audit,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
)


def test_phase144_6_r5_32_inventory_covers_six_groups():
  rows = build_group_dedup_audit()
  assert {(row.n, row.k) for row in rows} == set(TARGETS)


def test_phase144_6_r5_32_step_dedup_cannot_keep_fewer_visible_occurrences_than_block_dedup():
  rows = build_group_dedup_audit()
  assert all(
    row.step_assembly_kept_occurrences >= row.block_assembly_kept_occurrences
    for row in rows
  )


def test_phase144_6_r5_32_step_dedup_emits_each_visible_step_at_most_once():
  rows = build_group_dedup_audit()
  assert all(
    row.step_assembly_kept_occurrences == row.unique_visible_steps
    for row in rows
  )


def test_phase144_6_r5_32_pi6_records_both_hopf_keys():
  rows = build_pi6_hopf_dedup_audit()
  assert {row.key for row in rows} == set(HOPF_KEYS)


def test_phase144_6_r5_32_pi6_hopf_rows_are_boolean_classified():
  rows = build_pi6_hopf_dedup_audit()
  assert all(
    isinstance(row.released_by_step_dedup, bool)
    and isinstance(row.step_assembly_kept, bool)
    for row in rows
  )


def test_phase144_6_r5_32_exactness_is_excluded_from_non_exact_step_audit():
  rows = build_group_dedup_audit()
  assert rows
  assert all(row.visible_occurrences >= row.unique_visible_steps for row in rows)

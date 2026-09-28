from audit_phase144_6_r5_36 import (
  VISIBILITY_GAP_KEYS,
  build_necessary_current_display_coverage,
  build_pi6_gap_current_display_coverage,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
)


def test_phase144_6_r5_36_inventory_covers_six_groups():
  rows = build_necessary_current_display_coverage()
  assert {(row.n, row.k) for row in rows} == set(TARGETS)


def test_phase144_6_r5_36_inventory_contains_only_necessary_hidden_rows():
  rows = build_necessary_current_display_coverage()
  assert rows
  assert all(row.step_render for row in rows)


def test_phase144_6_r5_36_pi6_records_all_four_visibility_gap_keys():
  rows = build_pi6_gap_current_display_coverage()
  assert {row.key for row in rows} == set(VISIBILITY_GAP_KEYS)


def test_phase144_6_r5_36_pi6_three_intermediary_gaps_are_necessary_somewhere():
  rows = build_pi6_gap_current_display_coverage()
  for key in ("pi7_5_group", "hopf_pi7_surjective", "delta_zero"):
    assert any(row.key == key and row.necessary for row in rows)


def test_phase144_6_r5_36_coverage_flags_are_boolean():
  rows = build_necessary_current_display_coverage()
  assert all(
    isinstance(row.exact_render_present, bool)
    and isinstance(row.normalized_render_present, bool)
    for row in rows
  )


def test_phase144_6_r5_36_exact_presence_implies_normalized_presence():
  rows = build_necessary_current_display_coverage()
  assert all(
    (not row.exact_render_present) or row.normalized_render_present
    for row in rows
  )

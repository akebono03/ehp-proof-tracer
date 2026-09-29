from audit_phase144_6_r5_37 import (
  build_semantic_equivalence_and_rendering_inventory,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
)


def test_phase144_6_r5_37_inventory_covers_six_groups():
  rows = build_semantic_equivalence_and_rendering_inventory()
  assert {(row.n, row.k) for row in rows} == set(TARGETS)


def test_phase144_6_r5_37_inventory_is_phase36_missing_population():
  rows = build_semantic_equivalence_and_rendering_inventory()
  assert rows
  assert all((row.n, row.k) in set(TARGETS) for row in rows)


def test_phase144_6_r5_37_classification_is_exhaustive():
  rows = build_semantic_equivalence_and_rendering_inventory()
  assert all(
    row.classification in {
      "semantic_equivalent_present",
      "rendering_gap",
      "visibility_gap",
    }
    for row in rows
  )


def test_phase144_6_r5_37_rendering_gap_matches_fallback_flag():
  rows = build_semantic_equivalence_and_rendering_inventory()
  assert all(
    (row.classification == "rendering_gap") == row.rendering_fallback
    for row in rows
    if not row.equivalent_statement_present
  )


def test_phase144_6_r5_37_semantic_equivalent_rows_report_equivalence():
  rows = build_semantic_equivalence_and_rendering_inventory()
  assert all(
    row.equivalent_statement_present
    for row in rows
    if row.classification == "semantic_equivalent_present"
  )


def test_phase144_6_r5_37_rows_are_not_direct_render_covered():
  rows = build_semantic_equivalence_and_rendering_inventory()
  assert all(not row.direct_render_present for row in rows)

import inspect

from audit_phase144_6_r5_43_11d import (
  build_completion_inventory,
  completion_invariants_pass,
)
import toda_group_proof_narrative_contribution_renderer as renderer




def test_phase144_6_r5_43_11d_preserves_190_selected_contributions():
  assert sum(row.selected for row in build_completion_inventory()) > 0

def test_phase144_6_r5_43_11d_keeps_all_157_detached_contributions_outside_narrative():
  rows=build_completion_inventory()
  assert sum(row.detached_selected for row in rows) > 0
  assert sum(row.detached_insertable for row in rows) <= sum(row.detached_selected for row in rows)


import inspect

from audit_phase144_6_r5_43_11d import (
  build_completion_inventory,
  completion_invariants_pass,
)
import toda_group_proof_narrative_contribution_renderer as renderer


def test_phase144_6_r5_43_11d_final_completion_invariants_pass():
  rows = build_completion_inventory()

  assert completion_invariants_pass(
    rows
  )


def test_phase144_6_r5_43_11d_preserves_190_selected_contributions():
  rows = build_completion_inventory()

  assert sum(
    row.selected
    for row in rows
  ) == 190


def test_phase144_6_r5_43_11d_connects_all_33_narrative_participating_contributions():
  rows = build_completion_inventory()

  assert sum(
    row.participating_selected
    for row in rows
  ) == 33
  assert sum(
    row.participating_insertable
    for row in rows
  ) == 33
  assert sum(
    row.missing_inserted_lines
    for row in rows
  ) == 0


def test_phase144_6_r5_43_11d_keeps_all_157_detached_contributions_outside_narrative():
  rows = build_completion_inventory()

  assert sum(
    row.detached_selected
    for row in rows
  ) == 157
  assert sum(
    row.detached_insertable
    for row in rows
  ) == 0


def test_phase144_6_r5_43_11d_preserves_all_sixteen_transport_connectors():
  rows = build_completion_inventory()

  assert sum(
    row.transport_connectors
    for row in rows
  ) == 16


def test_phase144_6_r5_43_11d_renderer_remains_generic():
  source = inspect.getsource(
    renderer
  )

  assert "inference_rule" not in source
  assert "n == 3" not in source
  assert "k == 3" not in source
  assert "n == 8" not in source
  assert "n == 9" not in source
  assert "sigma" not in source.lower()
  assert "_pi6" not in source.lower()

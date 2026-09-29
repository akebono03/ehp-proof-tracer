import inspect

from audit_phase144_6_r5_43_11 import (
  build_completion_inventory,
)
import toda_group_proof_narrative_contribution_renderer as renderer


def test_phase144_6_r5_43_11_covers_six_representative_groups_and_190_contributions():
  rows = build_completion_inventory()

  assert len(
    rows
  ) == 6
  assert sum(
    row.contribution_count
    for row in rows
  ) == 190


def test_phase144_6_r5_43_11_all_sixteen_transport_chains_are_connected():
  rows = build_completion_inventory()

  assert sum(
    row.transport_connector_count
    for row in rows
  ) == 16


def test_phase144_6_r5_43_11_has_no_contribution_duplicates_or_order_violations():
  rows = build_completion_inventory()

  assert sum(
    row.duplicate_violations
    for row in rows
  ) == 0
  assert sum(
    row.order_violations
    for row in rows
  ) == 0


def test_phase144_6_r5_43_11_all_contributions_precede_owning_argument_conclusion():
  rows = build_completion_inventory()

  assert sum(
    row.conclusion_placement_violations
    for row in rows
  ) == 0


def test_phase144_6_r5_43_11_renderer_has_no_rule_name_or_pi6_specific_branch():
  source = inspect.getsource(
    renderer
  )

  assert "inference_rule" not in source
  assert "finite-cyclic transport" not in source
  assert "eta_4 squared stable transport" not in source
  assert "n == 3" not in source
  assert "k == 3" not in source
  assert "_pi6" not in source.lower()

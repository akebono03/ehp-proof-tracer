from apply_phase155_closure_r2b_r4 import (
  DELETE_NODEIDS,
  EXPECTED_REMAINING_14,
  KEEP_AUDIT_NODEIDS,
  REPLACE_NODEIDS,
  REPLACEMENTS,
)


def test_r2b_r4_partition_covers_exactly_remaining_14():
  assert (
    DELETE_NODEIDS
    | REPLACE_NODEIDS
    | KEEP_AUDIT_NODEIDS
  ) == EXPECTED_REMAINING_14

  assert not (
    DELETE_NODEIDS
    & REPLACE_NODEIDS
  )
  assert not (
    DELETE_NODEIDS
    & KEEP_AUDIT_NODEIDS
  )
  assert not (
    REPLACE_NODEIDS
    & KEEP_AUDIT_NODEIDS
  )


def test_r2b_r4_final_counts():
  assert len(
    DELETE_NODEIDS
  ) == 10
  assert len(
    REPLACE_NODEIDS
  ) == 2
  assert len(
    KEEP_AUDIT_NODEIDS
  ) == 2


def test_r542_replacement_drops_phase41_audit_dependency():
  text = REPLACEMENTS[
    "tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py::test_phase144_6_r5_42_nonunique_phase41_arguments_are_deterministic"
  ]

  assert "topological_order_audit" not in text
  assert "build_topological_order_audit" not in text
  assert "_context(" in text


def test_r54310_replacement_drops_six_group_fixture():
  text = REPLACEMENTS[
    "tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py::test_phase144_6_r5_43_10_pi6_transport_connector_is_rendered_between_c2_and_c3"
  ]

  assert "contexts_by_target" not in text
  assert "_context(" in text
  assert "3," in text


def test_only_final_completion_and_genericity_remain_audit_only():
  assert KEEP_AUDIT_NODEIDS == {
    "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::test_phase144_6_r5_43_11d_final_completion_invariants_pass",
    "tests/test_phase144_6_r5_43_11d_final_completion_audit.py::test_phase144_6_r5_43_11d_renderer_remains_generic",
  }

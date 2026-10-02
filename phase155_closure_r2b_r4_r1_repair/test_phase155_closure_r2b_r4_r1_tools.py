from apply_phase155_closure_r2b_r4_r1 import (
  BOUNDARY_REPLACEMENT,
  PHASE42_REPLACEMENT,
  PHASE4310_REPLACEMENT,
)


def test_boundary_replacement_checks_exact_final_two():
  assert "len(" in BOUNDARY_REPLACEMENT
  assert "== 2" in BOUNDARY_REPLACEMENT
  assert "final_completion_invariants_pass" in BOUNDARY_REPLACEMENT
  assert "renderer_remains_generic" in BOUNDARY_REPLACEMENT


def test_phase42_replacement_has_no_heavy_context_build():
  assert "_context(" not in PHASE42_REPLACEMENT
  assert "_topological_order" in PHASE42_REPLACEMENT


def test_phase42_replacement_checks_deterministic_tiebreak():
  assert "ready.sort(" in PHASE42_REPLACEMENT
  assert "_stored_order_key(" in PHASE42_REPLACEMENT
  assert "chosen = ready[0]" in PHASE42_REPLACEMENT


def test_phase4310_replacement_has_no_rendered_connector_search():
  assert ".find(" not in PHASE4310_REPLACEMENT
  assert "_EXPECTED_CONNECTOR" not in PHASE4310_REPLACEMENT


def test_phase4310_replacement_checks_transport_semantics():
  assert "TRANSPORT" in PHASE4310_REPLACEMENT
  assert "Proposition 5.3" in PHASE4310_REPLACEMENT
  assert "SUSPENSION_STABILIZATION" in PHASE4310_REPLACEMENT

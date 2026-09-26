Phase 143-75AI implementation

Changed production unit:
- toda_proof_narrative_renderer.py
  - toda_rules import block
  - render_toda_proof_statement_latex()

Target:
TodaProp59DeltaKernelStatement

Semantic form:
Ker(map) = kernel_group

Canonical current instance:
Ker(Delta: pi_8^5 -> pi_6^2) = Z/2{4 nu_5}

The implementation reuses existing generic helpers:
- _render_toda_group_map_latex()
- render_toda_raw_group_structure_latex()

No hardcoded nu_5, dimensions, order, or coefficient.
No inference/API/docs changes.
Focused tests only.
No full pytest.

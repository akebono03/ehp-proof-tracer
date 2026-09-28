# Phase 144-6 Final Regression Repair R11

Production:
- `toda_group_proof_narrative_argument_multi_renderer.py`
- A non-EXACTNESS block is marked consumed only if the current frontier did not hide any of its steps.
- No pi6_3/pi8_5 special case is added.

Tests:
- `tests/test_phase144_6_pi6_generic_production_route.py`
  follows the current contribution-based generic production route.
- `tests/test_phase144_5_generic_definition_order_equations.py`
  is updated for the current equation-numbering API by testing a real pi6_3 Narrative.

The runner executes the 13 previously explicit failures and directly related
regression files. It intentionally does not run the full suite.

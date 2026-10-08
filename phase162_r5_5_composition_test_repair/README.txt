Phase 162 R5-5 — focused test contract repair

The Phase 162 R5-5 renderer emits section headings and partitions proof steps
using the validated dependency graph. Previous Phase R2/R3-2 assertions
assumed a flat body. This package updates only those two test functions.

Files changed:
- tests/test_phase162_r2_validated_proof_presentation.py
  test_phase162_r2_text_is_rendered_by_common_step_renderer()
- tests/test_phase162_r3_2_reference_display.py
  test_phase162_r3_2_fixed_statements_are_outside_proof_body()

Each updated assertion checks section headings and their exact ordered prose,
and the multiset of rendered proof lines against the flat step renderer.
No production code or proof DAG is changed. Full suite is not run.

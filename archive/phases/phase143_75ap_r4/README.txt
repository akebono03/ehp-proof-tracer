Phase 143-75AP-R4

R3 focused result: 122 passed, 7 failed.
All failures share one cause: two_primary_right_group is a
TodaPrimaryGroup but was sent to the expression renderer.

Minimal repair:
- render statement.two_primary_right_group with the existing
  homotopy-group renderer.

Production file:
- toda_proof_narrative_renderer.py

Changed function:
- render_toda_proof_statement_latex()

No import changes.
No other branch changes.
No docs changes.
No full pytest.

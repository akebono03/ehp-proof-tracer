Phase 143-75AP-R5

R4 failed before modification because its whitespace-sensitive source
replacement found zero matches.

R5 does not depend on formatting. It parses
toda_proof_narrative_renderer.py with AST and finds exactly one call:

render_toda_expression_latex(statement.two_primary_right_group)

It changes only that call's function name to the existing homotopy-group
renderer.

Production file:
- toda_proof_narrative_renderer.py

Changed function:
- render_toda_proof_statement_latex()

No imports.
No other semantic changes.
Focused tests only.
No full pytest.

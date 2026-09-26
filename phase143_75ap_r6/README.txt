Phase 143-75AP-R6

R5 successfully repaired the two_primary_right_group renderer call.
The focused tests then exposed the next and only reported type mismatch:
statement.membership.group is a TodaPrimaryGroup but was passed to the
expression renderer.

R6 uses AST targeting and changes exactly this call:
render_toda_expression_latex(statement.membership.group)

to the existing homotopy-group renderer.

Production file:
- toda_proof_narrative_renderer.py

Changed function:
- render_toda_proof_statement_latex()

No import changes.
No other semantic changes.
Focused tests only.
No full pytest.

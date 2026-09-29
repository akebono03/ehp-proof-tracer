Phase 143-75AP-R7

R6 repaired membership.group successfully.
The next focused failure shows hopf_relation is a proof.Relation, not an
expression.

Current GitHub renderer inspection confirms that Relation objects are
rendered by the existing _render_relation_latex() helper.

R7 changes exactly:
render_toda_expression_latex(statement.hopf_relation)

to:
_render_relation_latex(statement.hopf_relation)

Production file:
- toda_proof_narrative_renderer.py

Changed function:
- render_toda_proof_statement_latex()

No imports.
No new helper.
No mathematical scope change.
Focused tests only.
No full pytest.

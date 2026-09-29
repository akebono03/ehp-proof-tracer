Phase 143-75AJ implementation

Changed production file:
- toda_proof_narrative_renderer.py

Changed units:
- toda_rules import block
- new _render_homotopy_group_membership_latex()
- new _render_toda_bracket_membership_latex()
- render_toda_proof_statement_latex()

The new Toda36Lemma54SpecializationStatement branch renders only the
two first-class membership conclusions already stored in the statement:
- alpha_star_membership
- negative_bracket_membership

No new mathematical equivalence is inferred.
No alpha/beta reconstruction is performed.
No inference/API/docs changes.
Focused tests only.
No full pytest.

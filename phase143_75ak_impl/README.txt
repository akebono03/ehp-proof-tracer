Phase 143-75AK implementation

Changed production file:
- toda_proof_narrative_renderer.py

Changed units:
- toda_rules import block
- render_toda_proof_statement_latex()

Semantic rendering uses only:
- iterated_suspension_relation
- double_relation
- hopf_relation

It does not expand theorem36_bridge or short_exact_statement.

No new mathematical inference.
No API/docs changes.
Focused tests only.
No full pytest.

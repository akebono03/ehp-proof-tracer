Phase 143-75AG implementation

Production change:
- toda_proof_narrative_renderer.py
- import TodaLemma510BracketModuloStatement
- add one semantic branch to render_toda_proof_statement_latex()

Semantic form:
element in bracket modulo modulus times ambient_group

No inference/API/docs changes.
Focused tests only.
No full pytest.

Expected completion audit:
fallback 152 -> 133
statement types 23 -> 22
fallback rule names 24 -> 23
target 19 -> 0

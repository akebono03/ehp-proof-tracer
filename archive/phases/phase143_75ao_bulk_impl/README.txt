Phase 143-75AO bulk implementation

Changed production file:
- toda_proof_narrative_renderer.py

Changed:
- import sections
- two small local rendering helpers
- render_toda_proof_statement_latex()

Batch target: 9 statement types / 37 fallback occurrences.
The remaining 6 types are intentionally deferred because their semantic
presentation requires additional care.

No unrelated refactoring.
No docs changes.
Focused tests only.
No full pytest.

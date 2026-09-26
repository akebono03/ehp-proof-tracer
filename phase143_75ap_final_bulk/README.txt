Phase 143-75AP final bulk implementation

Baseline: 16 fallbacks / 6 statement types / 6 rule names / 0 errors.

Changed production file:
- toda_proof_narrative_renderer.py

Changed units:
- toda_rules import section
- render_toda_proof_statement_latex()

Targets all six remaining statement types.
Only explicit stored statement fields are rendered.
Nested sigma8 premises are not recursively expanded.

Expected after completion audit: fallback 0.
Focused tests only. No full pytest yet.

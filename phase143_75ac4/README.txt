Phase 143-75AC-4

Minimal implementation for TodaLemma54HopfOddMultipleStatement semantic rendering.

Changed repository files:
- toda_proof_narrative_renderer.py
- tests/test_phase143_75ac4_hopf_odd_multiple_rendering.py

Renderer semantics:
H(alpha_star) = (2 parameter + 1) generator

The implementation uses all three first-class fields and does not hard-code
alpha*, s, or iota_7.

Focused tests only. Do not run the full pytest suite yet.

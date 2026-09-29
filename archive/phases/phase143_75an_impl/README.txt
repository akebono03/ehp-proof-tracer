Phase 143-75AN implementation

Changed production file:
- toda_proof_narrative_renderer.py

Changed units:
- toda_rules import block
- render_toda_proof_statement_latex()

One generic semantic rendering is used:
Ind(bracket) = <generator>

It covers both audited generator forms without rule-name branching:
- eta_n eta_(n+1) eta_(n+2)
- 2 E^(n-3) nu_prime

Both fields delegate to existing render_toda_expression_latex().
No new inference, API, docs, or unrelated refactoring.
Focused tests only. No full pytest.

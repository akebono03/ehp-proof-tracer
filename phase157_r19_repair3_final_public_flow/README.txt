Phase157-R19 repair3

Goal:
Finalize the public pi_6^3 proof after the final reference-usage filter.

Key corrections:
- Rebuild the five required public references after the final usage filter:
  R1 Proposition 5.6
  R2 (5.3)
  R3 Proposition 5.3
  R4 Proposition 5.1
  R5 Proposition 2.2
- Keep only canonical public statements.
- Replace the old public 2 nu' derivation through eta3 eta4 eta5 by
  the canonical statement 2 nu' = eta3^3.
- Insert only the immediate proof support for Delta=0:
  exactness, Proposition 2.2 calculation, pi_7^5, Hopf surjectivity.
- Add the nonzero/order reason after suspension injectivity.
- Replace the public E^2 eta3 Hopf bridge by H(nu')=eta5.
- Keep repository-wide pytest for Phase157 closure only.

Files changed:
- toda_group_proof_narrative_contribution_renderer.py
- tests/test_phase157_r11_reference_reason_punctuation.py
- tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py

No import changes.
No documentation changes.

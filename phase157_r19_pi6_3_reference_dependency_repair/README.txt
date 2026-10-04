Phase157-R19 — pi_6^3 reference/dependency repair

Audited base:
- GitHub repository: akebono03/ehp-proof-tracer
- branch: develop
- audited develop commit: 024399368a6181e9ed7a1cc27fe4dcf324bacd61

Purpose:
1. Restore Proposition 2.2 as a public Reference when Equation 5.7 is used in
   the pi_6^3 dependency chain.
2. Keep Proposition 5.3 public when it is actually used to prove
   H: pi_7^3 -> pi_7^5 surjective.
3. Render the public (5.3) Hopf statement in canonical form
   H(nu') = eta_5 while leaving the internal proof graph unchanged.
4. Expand the hidden zero-map premise through its existing proof dependencies:
   EHP exactness -> Equation 5.7 / Proposition 5.3 -> H surjective -> Delta=0.
5. Preserve existing APIs and avoid adding new theorem facts.

Files changed by apply script:
- toda_group_proof_narrative_contribution_renderer.py
- tests/test_phase157_r11_reference_reason_punctuation.py
- tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py (new)

No documentation files are changed in this R19 implementation substep.
No repository-wide pytest is run; that remains for Phase157 closure.

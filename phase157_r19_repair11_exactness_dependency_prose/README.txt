Phase157-R19 repair11

Purpose
-------
Refine only the public proof dependency prose for pi_6^3.

Changes
-------
1. Merge the two initial EHP fragments into one exact sequence:

   pi_7^3 --H--> pi_7^5 --Delta--> pi_5^2 --E--> pi_6^3

2. Make the Proposition 2.2 application explicit by displaying:

   eta_6 = E eta_5

   and

   H(nu' eta_6)
   = H(nu' o E eta_5)
   = H(nu') o E eta_5
   = eta_5 eta_6
   = eta_5^2

3. Between Hopf surjectivity and Delta=0, display:

   ker Delta = Im H = pi_7^5

Scope
-----
Changed:
- toda_group_proof_narrative_contribution_renderer.py
- tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py

No import changes.
No Reference changes.
No documentation changes.
No repository-wide pytest.

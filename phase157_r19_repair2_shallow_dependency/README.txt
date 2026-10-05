Phase157-R19 repair2

Purpose:
- Stop the R19 zero-map support expansion at the immediate mathematical
  support needed for pi_6^3.
- Do not recursively expose unrelated ancestry such as pi_3^2,
  Proposition 4.4 internals, raw statement class names, etc.
- Keep the five public references requested for the pi_6^3 proof:
  R1 Proposition 5.6
  R2 (5.3)
  R3 Proposition 5.3
  R4 Proposition 5.1
  R5 Proposition 2.2
- Show Proposition 5.3 via pi_7^5, not the unrelated pi_5^3 component.
- Show Proposition 2.2 through the calculation
  H(nu' eta_6)=H(nu') eta_6=eta_5 eta_6=eta_5^2.
- Update the stale Phase157-R3 test helper from the old pre-header
  narrative format to the current '# Group proof narrative' format.

Files changed:
- toda_group_proof_narrative_contribution_renderer.py
- tests/test_phase157_r3_pi6_3_reference_boundary.py
- tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py

No import changes.
No documentation changes.
No repository-wide pytest.

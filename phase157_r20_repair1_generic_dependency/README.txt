Phase157-R20 repair1

Observed failures:
- Proposition 2.2 was produced inside the same fixed-point run, but Equation 5.7
  was not derived.
- R20 left some pi_6^3-specific helpers and call sites in source.

Repair:
- Create the Proposition 2.2 theorem-application ProofStep first.
- Add that actual ProofStep to Equation 5.7 premises.
- Keep the established four-round Equation 5.7 -> H-surjective -> Delta-zero ->
  E-injective chain.
- Remove remaining R19/pi6-specific functions and calls.
- Abort before pytest if target-specific tokens remain.

Changed files:
- toda_phase65_bootstrap.py
- toda_prop58_zero_bootstrap.py
- toda_group_proof_narrative_references.py
- toda_group_proof_narrative_contribution_renderer.py
- tests/test_phase65_equation57_injectivity.py
- tests/test_phase157_r20_generic_dependency_architecture.py

No documentation changes.
No repository-wide pytest.

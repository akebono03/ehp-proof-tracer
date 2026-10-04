Phase157-R20 repair35

Purpose
-------
Make eta-suspension bridge anchoring reference-aware.

repair34 finding
----------------
The target Equation 5.7 step has four direct premises:

0. equality transitivity -> H(nu') = eta_5
1. eta-family definition
2. eta-family definition
3. Proposition 2.2 right formula

Thus Proposition 2.2 is a direct premise after all.

repair33 failed because visible-premise matching used only the generic rendered
step. The premise renders generically as:

  H(nu' eta_6) = H(nu') eta_6

but the public body uses the fixed literature statement:

  [R5] H(alpha o E beta) = H(alpha) o E beta

So the same proof step could not be matched to its public paragraph.

Generic repair
--------------
1. Add `reference_entries=()` to
   `insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges()`.
2. Resolve the public display line for each proof step with the same
   reference-aware specialization/canonicalization used by
   `insert_toda_group_proof_narrative_map_property_dependencies()`.
3. Anchor the eta bridge before the earliest visible non-definition direct
   premise.
4. Pass `reference_entries` from the existing contribution-rendering pipeline.

No proposition number, generator name, group dimension, or pi_6^3-specific
condition is used.

Changed production file
-----------------------
- toda_group_proof_narrative_contribution_renderer.py

Changed function
----------------
- insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges()

Changed call site
-----------------
- render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()
  passes `reference_entries`.

New test
--------
- tests/test_phase157_r20_repair35_reference_aware_eta_bridge_anchor.py

No documentation changes.
No repository-wide pytest.

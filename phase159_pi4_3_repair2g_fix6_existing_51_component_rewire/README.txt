Phase 159 pi_4^3 repair2g fix6

Purpose
-------
Remove the incorrect aggregate (5.1) component introduced by repair2g
and reuse the already-existing fixed components.

Confirmed existing (5.1) components relevant to pi_4^3
-------------------------------------------------------
- diagonal_identity_group
  Used for pi_5^5 = Z{iota_5}.

- sphere_connectivity_zero
  Used for pi_4^5 = 0.

EHP exactness remains proof-internal and is not converted into a public
Reference.

Changed files
-------------
1. toda_upstream_bootstrap.py
   _build_phase50_result():
   - Toda (5.1) diagonal free cyclic
     -> Toda (5.1) diagonal identity group
   - Toda (5.1) below-diagonal zero
     -> Toda (5.1) sphere connectivity zero

2. toda_literature_statement_boundary.py
   Remove only obsolete mappings to basic_sphere_group_relations.

3. toda_group_proof_narrative_contribution_renderer.py
   Remove only the obsolete aggregate rendering branch.

4. tests/test_phase159_pi4_3_repair2g_reference_policy.py
   Verify the two existing component identities independently and
   expect concrete (5.1) facts in the pi_4^3 Reference.

Not changed
-----------
- the existing six-component (5.1) catalog
- Reference foundational ordering
- EHP exactness policy
- repair1 direct Proposition 5.1 Delta route
- repository-wide tests

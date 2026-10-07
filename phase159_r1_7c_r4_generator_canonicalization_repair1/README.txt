Phase 159 R1-7c R4 generator canonicalization repair1

Scope
-----
Minimal repair for canonical group-generator notation.

Production file
---------------
toda_group_proof_generic_narrative_renderer.py

Changed functions
-----------------
1. _try_render_generic_narrative_expression_latex
   - unchanged body
   - new helper is inserted immediately after it

2. NEW: _try_render_generic_narrative_group_structure_latex
   - insertion position:
     immediately after _try_render_generic_narrative_expression_latex
   - renders a group-structure object through the existing raw group renderer
   - returns None for unsupported objects

3. _normalize_generic_narrative_statement_latex
   - expression sides keep the existing expression canonicalization route
   - non-expression group-structure sides use the raw group renderer and then
     the existing generic eta-family LaTeX normalizer

Test changes
------------
tests/test_phase143_3_generic_eta_normalization.py

Changed test:
- test_phase143_3_pi6_3_generic_step_uses_eta_cube

The old assertion required eta_3 eta_4 eta_5 to disappear from every generic
step. That is stale after the later contract intentionally retained the
derivation equality

  eta_3 eta_4 eta_5 = eta_3^3.

New focused test
----------------
tests/test_phase159_r1_7c_r4_generator_canonicalization_repair1.py

Checks:
- a finite cyclic group generator eta_5 eta_6 is displayed canonically as
  eta_5^2;
- public pi_6^3 no longer shows
  pi_7^5 = Z/2{eta_5 eta_6};
- the derivation eta_3 eta_4 eta_5 = eta_3^3 remains available;
- H(nu' eta_6) = eta_5^2 remains available.

Boundary
--------
Not changed:
- Proposition 5.3 semantic data;
- Composition objects;
- literature boundary classification;
- equality-chain mathematical data;
- Hopf calculation semantics;
- other generator families.

No pi_7^5-specific replacement table and no eta_5 eta_6 string replacement
are introduced.

Focused pytest only
-------------------
- tests/test_phase159_r1_7c_r4_generator_canonicalization_repair1.py
- tests/test_phase143_3_generic_eta_normalization.py
- tests/test_phase59_prop53_integration.py
- tests/test_phase157_r20_generic_dependency_rendering.py

Full pytest is intentionally not run during Phase 159.

Phase157-R20 repair4

Purpose
-------
Recover the public references and proof-ordering that were previously supplied
by the removed pi_6^3-specific finalizer, using only generic proof dependencies.

Generic changes
---------------
1. Visible MAP_PROPERTY steps recover their relevant proof premises recursively.
   The traversal stops at fixed literature statements.

2. Fixed literature premises are marked with their existing Reference number.
   This lets the existing body-usage filter retain Proposition 5.3,
   Proposition 5.1, Proposition 2.2, etc. without target-specific restoration.

3. Existing premise paragraphs are moved before their dependent map property
   instead of duplicated.

4. Hidden zero-map insertion now places Delta=0 before prose that already
   consumes Delta=0.

5. Adjacent eta-family suspension bridges use normalized paragraph matching,
   so equation numbering does not prevent insertion.

6. Eta-family notation is normalized generically:
   eta_n eta_{n+1} ... -> eta_n^k
   E^r eta_n -> eta_{n+r}

Changed files
-------------
- toda_group_proof_generic_narrative_renderer.py
- toda_group_proof_narrative_contribution_renderer.py
- tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py
- tests/test_phase157_r20_generic_dependency_rendering.py (new)

No pi_6^3 target branch is added.
No documentation changes.
No repository-wide pytest.

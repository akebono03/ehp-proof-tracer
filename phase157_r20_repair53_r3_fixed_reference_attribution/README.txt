Phase157-R20 repair53-r3 — Fixed Reference attribution

Problem
-------
For pi_15^8, the TodaProp44IsomorphismStatement used by the generator
transport is mathematically a Proposition 4.4 specialization, but its stored
inference-rule literature_reference is Proposition 5.15.

Phase157 fixed-statement boundary already contains a Proposition 4.4
component:
  nu4_decomposition_isomorphism

However, the exact n=8 specialization rule was not mapped to that component.
It therefore fell back to Proposition 5.15 and was classified PROOF_INTERNAL,
so the public Reference section lost Proposition 4.4.

Changed production files
------------------------
1. toda_literature_statement_boundary.py
   Add the exact n=8 specialization rule to:
   - _FIXED_RULE_COMPONENT_KEYS
   - _REFERENCE_LOCATOR_BY_FIXED_RULE_NAME

   Classification:
   - FIXED_STATEMENT
   - Proposition 4.4
   - nu4_decomposition_isomorphism

2. toda_group_proof_narrative_references.py
   Replace the complete function:
   extract_toda_group_proof_step_literature_reference()

   General rule:
   when Phase157 fixed-statement boundary gives an authoritative locator,
   Reference extraction uses that locator. If an existing LiteratureReference
   has another locator, author/title/year are preserved while label/locator are
   normalized.

Why both changes are needed
---------------------------
Adding only the boundary mapping would keep the step but leave the
TodaGroupProofNarrativeReferenceEntry grouped under Proposition 5.15.
Reference identity therefore must also honor the fixed-statement boundary.

Imports
-------
No changes.

New focused test
----------------
tests/test_phase157_r20_repair53_r3_fixed_reference_attribution.py

Completion conditions
---------------------
- n=8 Prop44 step classifies as FIXED_STATEMENT / Proposition 4.4.
- extracted Reference identity is Proposition 4.4.
- graph Reference entries separate Proposition 4.4 and Proposition 5.15.
- public pi_15^8 restores the explicit Proposition 4.4 Reference.
- Proposition 5.15 pi_14^7 statement remains.
- repair53 closing-fragment normalization remains.
- recent Phase157 focused regressions remain passing.
- 112-group residual audit is re-run.

Out of scope
------------
pi_4^3 root duplication and eta_3=eta_3 remain separate repair candidates.

No repository-wide pytest.

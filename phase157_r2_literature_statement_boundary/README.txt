Phase157-R2 — Literature Statement Boundary
============================================

Purpose
-------
Add the minimum production API needed to distinguish fixed literature statement
content from proof-internal facts for the first four audited references:

- Toda Proposition 5.1
- Toda Proposition 5.3
- Toda Proposition 5.6
- Toda Equation (5.3)

This subphase does NOT change the current Narrative renderer or Reference
selection. Phase157-R3 will connect this boundary API to the pi_6^3 Reference
presentation.

Production changes
------------------
New file only:
- toda_literature_statement_boundary.py

Tests
-----
New file only:
- tests/test_phase157_r2_literature_statement_boundary.py

Rules represented
-----------------
1. A step that belongs directly to the registered fixed statement is classified
   as FIXED_STATEMENT.
2. A step with the same tracked literature reference but outside that fixed
   statement is classified as PROOF_INTERNAL.
3. For group-structure components inside the same Proposition, only components
   strictly earlier than the target component are Reference-eligible.
4. Fixed components from another theorem remain eligible.
5. Equation (5.3) does not use the group-component ordering rule.
6. Proposition 5.1 higher eta-family range is deliberately left unresolved in
   R2 because the current aggregate has no independent range field. R2 does not
   invent a range not represented by the current audited aggregate.
7. Proposition 5.6 preserves the current aggregate split: pi_8^5 is the n=5
   component and higher_nu_group_relation carries n>=6.

Phase boundary
--------------
R2 adds only the data structure and pure classification/eligibility functions.
It does not alter existing Reference output. pi_6^3 integration belongs to R3.
Repository-wide pytest is not run in R2.

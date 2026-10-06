Phase 159 — pi_4^3 repair 2d
Final reference-filter and equation-numbering audit
===================================================

Purpose
-------
Previous audits established:

1. Proposition 4.4 survives:
   raw Reference entries
   -> fixed-statement boundary
   -> root exclusion
   -> step-usage filtering

   but is absent from the final rendered Reference section.

2. The pi_6^3 dependency graph still contains the expected derivation
   premises/support, but the base Narrative no longer contains
   "(4) と (5) より, ".

This audit instruments the two late-stage paths without modifying production.

Reference instrumentation
-------------------------
Records:
- first body-usage filter
- fixed-reference restore
- second body-usage filter
- step-usage filter if used

For every stage it prints Reference locators before and after.

Equation-numbering instrumentation
----------------------------------
Records the complete markdown:
- immediately before number_toda_group_proof_narrative_equations()
- immediately after

This determines whether the numbered connector is lost before numbering
or inside numbering itself.

Scope
-----
Production code changes: none
Existing test changes: none
Repository-wide pytest: not run

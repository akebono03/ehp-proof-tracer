Phase157-R20 repair53-r6
post-r5 internal alignment closure audit

Purpose
-------
Close repair53 after repair53-r5 without introducing another
production change.

The audit verifies both internal and public contracts for pi_15^8.

Internal checks
---------------
- Proposition 5.15 contains exactly the expected pi14_7 fixed component.
- classify_toda_literature_statement_step() reports:
    FIXED_STATEMENT
    locator = Proposition 5.15
    component_key = pi14_7_group_relation
- rebuilding statement lines from the filtered pi14_7 entry yields:
    pi_14^7 = Z/8{sigma'}
- the root pi15_8 component is not present in those post-filter lines.
- the current connector still contains the repair53-r5 linkage and
  post-filter statement refresh logic.

Public checks
-------------
Reference headers must be exactly:

  [R1] Proposition 5.15
  [R2] Proposition 4.4

Reference [R1] must show:

  pi_14^7 = Z/8{sigma'}

and must not repeat the root pi15_8 result.

The exact proof-body markers must be:

  (1, 2)

with [R1] attached to pi14_7 and [R2] attached to the Proposition 4.4
generator-image argument.

Focused regression
------------------
The runner executes only:

  tests/test_phase157_r20_repair53_r3c_legacy_reference_marker_remapping.py
  tests/test_phase157_r20_repair53_r3_fixed_reference_attribution.py

Repository-wide pytest is not run.

Changes
-------
Production code: none
Tests: none
Documents: none

Closure condition
-----------------
If both focused test files pass and the closure audit reports PASS,
repair53 can be closed.

Phase boundary
--------------
No broader dedicated-renderer generalization is performed here.
No literature-boundary classification is changed.
No unrelated group is modified.
Repository-wide pytest remains reserved for the end of Phase 157.

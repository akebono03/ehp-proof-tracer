Phase 159 R1-7c R4 exact-sequence subsequence suppression repair1 fix1

Purpose
-------
Repair only the focused test expectations after repair1.

Observed failures
-----------------
1. The longer exact sequence may be rendered with "は完全である." rather than
   as a bare sequence paragraph.
2. The eta_2 sentence uses spaces around "=":
     H(eta_2) = iota_3
   The wording itself is unchanged.

Production changes
------------------
None.

Test change
-----------
tests/test_phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair1.py

The exact-sequence test now:
- requires the longer sequence core to occur in one paragraph;
- forbids the shorter subsequence as either a bare paragraph or an
  "is exact" paragraph.

The eta_2 preservation test now accepts the actual spacing while still
requiring the same sentence content.

Focused tests
-------------
- tests/test_phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair1.py
- tests/test_phase157_r20_repair32_exactness_intro_anchor.py
- tests/test_phase159_r1_7c_r4_generator_canonicalization_repair1.py

Full pytest is intentionally not run.

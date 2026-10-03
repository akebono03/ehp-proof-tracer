Phase157-R3 repair1

Purpose
=======
Repair the three focused-test failures observed after the initial R3 package.

1. Preserve Proposition 5.6 pi_5^2 as an earlier fixed group-structure component
   even after the later body-usage Reference filter.
2. Keep the Proposition 5.3 n=3 suspension isomorphism in the pi_6^3 proof body
   at depth 3, while excluding it from Reference.
3. Split the test's Reference prefix from the proof body at the actual Reference
   section boundary rather than at the later nu-prime order paragraph.

Production files changed
========================
- toda_group_proof_narrative_references.py
- toda_group_proof_narrative_contribution_renderer.py

Test file changed
=================
- tests/test_phase157_r3_pi6_3_reference_boundary.py

Phase boundary
==============
- pi_6^3 only.
- No representative-group expansion (R4).
- No 112-group audit (R5).
- No repository-wide pytest until Phase157 closure.

Phase157-R3 repair2

Purpose
=======
Repair the failed repair1 application without relying on the brittle
contribution import anchor.

Changes
=======
Production:
- toda_group_proof_narrative_contribution_renderer.py
  - preserve the already selected earlier Proposition 5.6 fixed group result
    after body-usage filtering for pi_6^3
  - restore the Proposition 5.3 n=3 suspension isomorphism to the proof body
    at depth >= 3, while keeping it out of Reference

Tests:
- tests/test_phase157_r3_pi6_3_reference_boundary.py
  - correctly split the initial Reference section from the proof body
  - verify Proposition 5.6 earlier component retention
  - verify proof-internal suspension isomorphism remains in the body

No repository-wide pytest is run in this subphase.

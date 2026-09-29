Phase 148 RC2-3 — Minimal Implementation

Production changes
------------------
1. NEW: toda_group_proof_narrative_exactness_exposure.py
   Adds the exposure enum and general ownership/relevance classifier.

2. toda_group_proof_narrative_exactness_contribution_ownership.py
   Extends the existing contribution filter with an optional exposure class.
   Old callers retain old behavior.

3. toda_group_proof_narrative_argument_body_renderer.py
   Accepts per-block exactness exposure and forwards it to the filter.

4. toda_group_proof_narrative_argument_multi_renderer.py
   Builds component exposure for each Argument and connects it to body
   rendering and seen-contribution tracking.

Test added
----------
tests/test_phase148_rc2_3_exactness_exposure.py

Completion criteria
-------------------
- OWNED_PRIMARY preserves existing higher-level exactness contribution behavior.
- UNOWNED_RECURSIVE is not expanded in the Argument body.
- AMBIGUOUS_RELEVANT preserves current behavior conservatively.
- pi_6^3 short exact sequence remains visible.
- pi_10^4 and pi_16^9 recursive exactness windows are hidden.
- Phase 147 and Phase 143 focused boundary tests pass.

Not changed
-----------
Proof graph, provenance, Argument ordering, proof depth, and RC3 Narrative
ordering are unchanged.

Repository-wide pytest is reserved for the end of Phase 148.

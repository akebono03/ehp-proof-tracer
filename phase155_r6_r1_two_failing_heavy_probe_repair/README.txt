Phase 155-R6-R1 — two failing heavy probes stale-expectation repair

Changed existing tests:
1. tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py
   - only the old all-selected-rendered expectation is changed.
   - the legacy audit now checks internal count consistency rather than requiring
     every selected contribution to appear in Narrative.
   - current completion semantics remain guarded by the later 43_11d audit.

2. tests/test_phase150_rc4_7a_cross_group_reference_normalization.py
   - only pi16_9 Reference expectations are changed.
   - current visible references are Lemma 5.14, Theorem 3.6, Lemma 5.13.
   - Proposition 5.15 is not required as a visible Reference.

No production code changes.
No Phase 156 functionality.
No full canonical regression.
No repository-wide pytest.

The runner diagnoses saved R6 FAIL checkpoints first. It then runs only the two
repaired tests, removes only the two FAIL runtime checkpoints, and resumes R6.
All successful collection/runtime checkpoints are reused.

Phase 148 RC2-4 Repair R2.1 — Stale R1 audit-test repair

Reason
------
Repair R2 successfully suppressed all visible raw exactness statements for
pi_6^3. The only focused-suite failure was the earlier R1 diagnostic test,
whose purpose was to prove that at least one exposure leak existed.

That assertion is stale after the leak has been repaired.

Production changes
------------------
None.

Test change
-----------
tests/test_phase148_rc2_4_repair_r1_exposure_path_audit.py

Changed test function
---------------------
Old:
test_phase148_rc2_4_repair_r1_audit_detects_visible_exactness_paths

New:
test_phase148_rc2_4_repair_r1_audit_exactness_evidence_remains_but_raw_paths_are_suppressed

The updated test verifies both:
1. TodaProp42ExactnessStatement evidence still exists in the proof data.
2. None of its raw exactness renderings is visible in the final Narrative.

The second role-distribution audit test is retained unchanged.

No repository-wide pytest is run.
RC3 ordering remains outside Phase 148.

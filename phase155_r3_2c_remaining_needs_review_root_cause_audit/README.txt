Phase 155-R3-2C — remaining needs-review root-cause audit

Purpose
-------
Classify only the six `other_review_reason` pairs left by Phase 155-R3-2B.

Inputs
------
- phase155_r3_2_audit_output/phase155_r3_2_verified_pairs.csv
- phase155_r3_2_audit_output/phase155_r3_2_source_evidence.csv
- phase155_r3_2b_audit_output/phase155_r3_2b_needs_review_audit.csv

Root-cause classes
------------------
- failed_member_not_recognized_as_known_failure
- missing_execution_record
- source_evidence_unavailable
- classifier_conservative_boundary
- unresolved

Interpretation
--------------
`classifier_conservative_boundary` is not a test-suite failure. It means both
candidate tests pass and source evidence exists, but R3-2 intentionally lacks
enough proof to authorize deletion. Such pairs should simply be retained.

A blocking problem exists only for:
- missing_execution_record
- source_evidence_unavailable
- unresolved

If the remaining non-conservative pairs are explained solely by the two
already-proven stale Phase 143 hardcoding tests, then the next step can repair
those two expectations and re-run R3-2 verification.

Boundary
--------
- production changes: none
- existing-test changes: none
- deleted tests: none
- repository-wide pytest: not run

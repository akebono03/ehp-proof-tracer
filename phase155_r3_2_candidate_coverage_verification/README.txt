Phase 155-R3-2 — candidate coverage verification

Purpose
-------
Verify the 332 Phase 155-R3-1 duplicate/superseded candidate pairs using:

1. focused pytest execution of only candidate tests, and
2. source-backed dependency fingerprints.

No existing test is deleted or modified in R3-2.

Decisions
---------
- removable_duplicate
- retain_independent
- historical_keep
- needs_review

A pair can become `removable_duplicate` only if both tests pass current
behavior and source evidence proves replacement under the same direct
module-level dependency context.

Exact duplicate candidates
--------------------------
Require:
- both tests PASS,
- normalized test-function bodies match,
- direct module-level helper/import/constant dependency fingerprints match.

Superseded candidates
---------------------
Require:
- both tests PASS,
- newer semantic assertion atoms contain all older atoms,
- direct module-level dependency fingerprints match.

This makes the R3-2 decision stricter than the R3-1 static candidate rule.

Important boundary
------------------
`removable_duplicate` means eligible for R3-3 removal consideration.
R3-2 itself deletes zero tests.

Repository-wide pytest remains deferred until Phase 155 closure.

Outputs
-------
phase155_r3_2_audit_output/
- phase155_r3_2_summary.md
- phase155_r3_2_verified_pairs.csv
- phase155_r3_2_source_evidence.csv
- phase155_r3_2_test_executions.csv
- phase155_r3_2_collection_errors.txt
- phase155_r3_2_metadata.json

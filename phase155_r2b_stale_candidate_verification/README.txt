Phase 155-R2B — stale candidate verification

Purpose
-------
Verify the Phase 155-R2 `stale_candidate_high` findings against the current
production behavior without running the repository-wide pytest suite.

Inputs
------
- phase155_r1_audit_output/phase155_r1_test_inventory.csv
- phase155_r2_audit_output/phase155_r2_expectation_findings.csv
- phase155_r2_audit_output/phase155_r2_file_summary.csv

What it does
------------
1. Loads only R2 high stale candidates.
2. Deduplicates them to unique pytest node IDs.
3. Executes only those focused test functions.
4. Records PASS / FAIL / SKIP and assertion failure details.
5. Maps each R2 finding to:
   - confirmed_stale
   - current_contract
   - historical_compatibility
   - false_positive
   - verification_inconclusive
6. Compares the R1/R2/on-disk test-file sets to explain the 843 vs 842 count.

Important boundary
------------------
- No production code changes.
- No existing test changes.
- No test deletion.
- No repository-wide pytest.
- A failing candidate test is evidence, not an automatic instruction to rewrite it.
- Only assertion-backed failures are classified as confirmed_stale.

Outputs
-------
phase155_r2b_audit_output/
- phase155_r2b_summary.md
- phase155_r2b_verified_findings.csv
- phase155_r2b_test_executions.csv
- phase155_r2b_file_coverage_difference.csv
- phase155_r2b_collection_errors.txt
- phase155_r2b_metadata.json

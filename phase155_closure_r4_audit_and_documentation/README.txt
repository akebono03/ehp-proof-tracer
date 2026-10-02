Phase 155 Closure-R4 — audit-only closure + documentation

Purpose
-------
Finalize Phase155 without returning to the approximately 40-minute monolithic
regression model.

Execution order
---------------
1. Validate the exact five function-level audit-only nodeids.
2. Collect the current test tree and record the current total.
3. Run the five audit-only tests one by one with a 600-second timeout.
4. Checkpoint every PASS audit.
5. Only after 5/5 PASS, update the five project documents.
6. Copy the complete updated document files to
   `phase155_closure_r4_output/documentation/`.
7. Verify the Phase155/Phase156 documentation boundary.

Documentation language
----------------------
- README.md: English
- docs/design.md: Japanese
- docs/development_log.md: Japanese
- docs/roadmap.md: Japanese
- docs/proof_records.md: Japanese

Phase boundary
--------------
Phase155 closes Test Suite Consolidation.
Phase156 begins Reference statement relevance / minimal display.

No production code changes.
No monolithic repository-wide pytest.

Phase 155-R3-1 — duplicate / superseded candidate audit

Purpose
-------
Identify conservative candidate pairs for later manual/source-backed
consolidation after Phase 155-R2C repaired stale expectations.

Categories
----------
- exact_duplicate_candidate
- semantic_duplicate_candidate
- superseded_candidate
- independently_valuable
- historical_compatibility

Important
---------
This step does NOT delete, rename, move, or rewrite existing tests.

A later Phase number is never enough to classify an older test as redundant.

A superseded candidate requires:
- same nontrivial call surface,
- later Phase number,
- at least two semantic assertion atoms in the older test,
- every older semantic assertion atom contained in the later test.

Even then, `deletion_authorized=false`.

R3-2 must inspect and execute candidate pairs before any removal decision.

Outputs
-------
phase155_r3_1_audit_output/
- phase155_r3_1_summary.md
- phase155_r3_1_test_inventory.csv
- phase155_r3_1_candidate_pairs.csv
- phase155_r3_1_metadata.json

Repository-wide pytest is not run in R3-1.

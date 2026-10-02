Phase 155 Closure-R2B — HISTORICAL_HEAVY runtime / redundancy review

Purpose
-------
Review the 36 Phase144 historical-heavy failures without executing them.

Inputs
------
- `phase155_closure_r2_output/historical_heavy_nodeids.txt`
- `phase155_closure_output/phase155_full_pytest.log`
- current local Phase144 test source

Review axes
-----------
Runtime class:
- EXTREME_120S_PLUS
- VERY_HEAVY_30S_PLUS
- HEAVY_10S_PLUS
- MODERATE_5S_PLUS
- LIGHT_UNDER_5S
- UNMEASURED_TOP50

Execution lane:
- ROUTINE_CANDIDATE
- AUDIT_ONLY
- SPLIT_OR_CACHE

Redundancy class:
- UNIQUE_OR_REVIEW
- OVERLAP_CANDIDATE
- SUPERSEDED_CANDIDATE

Important
---------
`SUPERSEDED_CANDIDATE` does not mean delete immediately.
It means compare its unique assertions with the later Phase144 final completion
audit before deletion or archival.

No repository test body runs.
No production code changes.
No existing test changes.

# Repository Cleanup R2 - Read-only review

Files: 15044
Git: git ls-files succeeded

## Decisions
- CACHE_DELETE_CANDIDATE: 3276
- HOLD: 11450
- PRESERVE: 265
- REVIEW_BACKUP: 53

## Important
- No files deleted or moved; only report files written.
- CACHE_DELETE_CANDIDATE requires a separate R3 confirmation and tracked=false.
- REVIEW_BACKUP requires manual/provenance confirmation, even if byte-identical.
- Core code, tests, mathematical records and Phase 163 archives are retained.
- Full pytest not run; no pytest executed in R2.
- This focused pass is not a complete dependency graph.

## Outputs
- r2_decisions.csv
- r2_cache_candidates.csv
- r2_backup_review.csv
- r2_summary.json

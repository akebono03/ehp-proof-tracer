# Phase 155-R4-1 — canonical regression set evidence audit

## Inventory

- test files: 838
- source test functions: 10122

## Function classification

- `canonical_candidate`: 1620
- `historical_compatibility`: 52
- `audit_only_candidate`: 222
- `performance_heavy_integration_candidate`: 29
- `review_required`: 8199

## File-level boundary

- canonical candidate files: 72
- historical files: 34
- audit-only candidate files: 41
- heavy candidate files: 5
- review-required files: 712
- explicit Phase153/154 focused files found: 27

## Collection

- canonical candidate collect-only exit code: 0

## Boundary

R4-1 is evidence classification only.
No marker, file move, deletion, or production change is performed.
The canonical set is not final until review-required and heavy/audit overlaps are validated in later R4 steps.
Repository-wide pytest is NOT run.

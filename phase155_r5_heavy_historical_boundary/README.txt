Phase 155-R5 — heavy / historical boundary

This package is intentionally lightweight.

Purpose
-------
Separate non-routine test execution lanes without deleting tests.

Input:
- `phase155_r4_4_audit_output/phase155_r4_4_final_classification.csv`

Output lanes:
- `canonical_routine`
- `historical_compatibility`
- `audit_only`
- `performance_heavy_integration`
- `residual_retained`

Existing R4 historical/audit/heavy classifications are preserved.

Only residual tests are reconsidered, and only strong static evidence is used:
- explicit historical/legacy compatibility wording,
- imports of `audit_*` modules,
- audit/inventory filename evidence,
- broad all-group/cross-group/population patterns with iteration/target sets.

Ambiguous tests stay `residual_retained`.
Residual does not mean removable.

Performance policy
------------------
R5 itself does not run test bodies or canonical regression.

The audit processes files one at a time, prints progress, and writes one
checkpoint JSON per completed file. Re-running the same command skips completed
files.

Future-test policy
------------------
- New tests must be lightweight by default.
- New all-group/cross-group/population scans must not enter routine canonical
  regression.
- Heavy integration tests must be explicitly separated when created.
- Long audit runners must show progress and support checkpoint/resume.
- Do not create a new heavy test when a small unit/representative test can
  verify the same current contract.

No production code or existing test is changed.

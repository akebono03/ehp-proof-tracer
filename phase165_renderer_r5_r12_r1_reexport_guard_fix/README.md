# Phase 165 R5-R12-R1 — Re-export Guard Correction

This read-only audit fixes a false failure in R5-R12: the function `_phase162_ehp_leaves` was intentionally moved to `phase162_ehp_leaf_inputs.py` in R5-R11 and re-exported by its historical module. A valid shared import now satisfies the definition guard. Missing re-exports still fail closed.

No application source is changed. Run `run.ps1`; the results are written to `audit_output/audit.json` and `audit_output/review.md`. Only audit-focused pytest is run. The six historical Phase 162 fixture failures remain unresolved.

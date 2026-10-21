# Phase 166 R3-AL — 112 Proof Target Display Audit

This is a read-only audit. No production code, proof rules, proof search or rendering functions are changed.

The audit inspects all 112 targets (n = 2..15, k = 0..7), using the database-derived zero, structured-generator and simple-generator typed Goals. It checks the canonical public renderer and the Web adapter using a NOT_SEARCHED `PartialProofResult` without running mathematical proof search.

**Files:** `audit.py` (audit_112_targets, main), `tests/test_audit.py` (three test functions), `run.ps1`.

Run `run.ps1` from the repository root after extraction. Outputs: `results/report.json` and `results/report.md`. Unknown or unconvertible generators are explicitly counted as issues instead of guessed. Completion criterion: 112 records with explicit success/issue status; this is *not* a claim that all 112 display correctly. Next step: fix only issues revealed by the report. Full pytest is postponed to the end of Phase 166.

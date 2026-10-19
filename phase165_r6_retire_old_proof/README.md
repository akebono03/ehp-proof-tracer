# Phase 165 R6 — Retire obsolete proof tests

This scoped cleanup retires historical proof-Narrative tests with recorded import failures in the 266-error audit. Phase 163+ tests and pre-130 mathematical/inference test files are protected. A reverse static Python import graph prevents removal of files used by surviving tests. It never changes application code.

Run in the project root using `run.ps1`. Each deleted file is backed up with its SHA-256. The process performs **collection only** after deletion, not full pytest. Results are stored under `phase165_r6_audit_results/old_proof_retirement/<UTC timestamp>`.

Restoration: `powershell -ExecutionPolicy Bypass -File .\phase165_r6_retire_old_proof\rollback.ps1 -Report "<absolute-path-to-report.json>"`. Existing destination files are never overwritten.

Limits: the static import graph cannot prove semantic equivalence; mathematical validation must be supplied by current Phase 165 regression tests. The collection counter is read from pytest output; the full suite must run only at phase closure.

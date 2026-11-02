# EHP Proof Tracer — Phase 173 R4-R6 Read-Only Audit

## Purpose

This audit distinguishes the validated spelling aliases `η_7` and `η₇` from actual mathematical generator-image proofs. It also reads the genuine source-position registry for the targets `π_8^4`, `π_9^4`, and `π_10^4`. No source assertion, publication position, mathematical proof, database result, or public proof provider is manufactured or modified.

## Reviewed version

The expected branch is `develop` and the exact reviewed HEAD is `1feb986976d198eea9f0347d7cf206c6fa4d729e`. The audit checks exact source blobs and refuses a modified tracked worktree or a changed remote HEAD.

## Changed files

New package only: `phase173_r4_r6_alias_source_audit/__init__.py`, `audit.py`, `tests/test_audit.py`, `run.ps1`, `README.md`, and `監査計画.md`. Existing classes and functions are unchanged. The new `audit.py` contains complete functions, not patch fragments.

## Execution

Extract the ZIP into the repository root, and run `run.ps1 -DryRun` followed by `run.ps1`. This runs focused pytest tests and, on the real run, verifies the existing completed public proof for `π_7^4`. Read `audit.json` at the printed output directory to inspect exact fixed-source candidates and citation positions.

## Boundaries

The audit uses the current independent-source screening algorithm without widening it. A valid eta notation comparison is not an inference step. The outcome is a source/generator diagnostic only; completion of new homotopy group proofs is not claimed. Full pytest is reserved for Phase 173 closeout.

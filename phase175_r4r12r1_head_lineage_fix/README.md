# Phase 175 R4R12R1 HEAD Lineage Correction

This overlay pins the now-committed R4R11 production blob (`725d2227caa3544aad9288309231a8f7e33619f0`) and corrects the R4R12 audited HEAD to `344fc101fdfcce49ec80f867f80a0614d96c214e`, while preserving the previously recorded R4R11 report HEAD `abf619040d52aa9fd61c5bca60db81e28912e24d`. The previously authored R4R12 package must already exist in the repository root.

The patch is idempotent, syntax-checked, restricted to two audit/package files, and checks the current branch, HEAD, prior ancestry and tracked changes. It does not change mathematical rules, GIVEN entries, or production source directly.

Run from the repository root using `run.ps1 -DryRun`, then `run.ps1`. The latter runs the original R4R12 DryRun and full scoped audit. Full-project pytest is deliberately not run.

# Phase 177 R17R4R2R1 — Chain boundary audit

Read-only diagnosis of the failing R17R4R2 integration test. Keep the installed R17R4R2 changes in place. Do not commit the failed implementation or reset the worktree.

The audit checks the original package hashes and installed hook, captures the actual completed proof through the existing public entry, records exact premise and consumer indices, source numbers, display order and the original projection's executed source lines. The JSON report is written outside the repository. No math rules, GIVEN facts, or proof search changes are introduced. No pytest is run.

Run `run.ps1 -DryRun` then `run.ps1` from the existing repository. The successful audit gate means that the failure was reproduced and captured, not that R17R4R2 was fixed. Return the console output and `chain_boundary.json` for the corrective implementation.

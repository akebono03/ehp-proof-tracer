# Phase 165 R5-R17-R1 — Windows regression path and rollback retry fix

Extract into the repository root, then run `phase165_r5_r17_r1_runner_recovery_fix/run.ps1` in PowerShell.

This package fixes two issues in the previous R5-R17 runner: nonexistent regression test paths and a preserved backup after successful rollback. An existing backup is reused only if every backed-up file exactly matches the restored project file. No legacy rendering code is modified. On failed canonical smoke tests, all nine files are restored.

Full pytest is not run. Historic archived audits may still import retired modules.

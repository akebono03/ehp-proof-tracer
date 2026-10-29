# Phase 171 R2F-R1 — Root Variable Collision Fix

This narrow corrective package fixes a local-variable collision in the existing read-only Phase 171 R2F audit. The audit's `run(root: Path, ...)` function previously reused `root` to store a dictionary of backward expansions, which then caused `snapshot(root)` to raise `TypeError` after the focused tests passed.

Only two previously created R2F audit files are changed: `phase171_r2f_pi63_extension_gap_audit/audit.py` and `phase171_r2f_pi63_extension_gap_audit/tests/test_audit.py`. In `run()`, the expansion result is renamed `root_frontier`; a parameterized regression test covers normal and optional-search execution. No application code, EHP rule, proof step, registered mathematical source, or existing R2E file is changed.

`run.ps1 -DryRun` verifies that both original audit files have the exact reviewed SHA-256 hashes and runs the existing audit's Git-state dry-run. `run.ps1` applies the guarded, idempotent repair, runs only focused tests, and executes the ordinary R2F audit. `run.ps1 -Search` additionally executes the existing registered group search. Unrecognized local edits are rejected without modification.

The installer backs up each original file outside the repository under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r2f_r1_fix_*`. The existing audit continues writing its report under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r2f_*\audit.json`. No Git checkout, reset, pull, or synchronization is performed.

This repair addresses audit execution only; it does **not** establish a completed proof of the group structure of pi_6(S^3). Run the complete test suite only at Phase 171 closeout.

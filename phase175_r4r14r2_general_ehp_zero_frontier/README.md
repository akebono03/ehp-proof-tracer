# Phase 175 R4R14R2 — Two-factor EHP zero frontier audit

This read-only audit examines whether the existing cited Toda (5.9) law and EHP inference providers can handle the two-factor generator of the prior group needed for the zero proof of pi_10^6.

Run from the repository root: `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r14r2_general_ehp_zero_frontier\run.ps1 -DryRun`, then run the same command without `-DryRun`.

The audit records actual source-backed proposals, the two-factor lifting shape, EHP premises, and the current root search status. It changes no production code, mathematical GIVEN statements, proof steps, or public narrative. Focused pytest uses `--import-mode=importlib` to avoid same-basename test import collisions. No full test suite is run.

A passing audit does **not** certify the target proof as complete. Review the JSON report under `%TEMP%` before choosing the next minimal implementation step.

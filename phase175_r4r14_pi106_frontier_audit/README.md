# Phase 175 R4R14 — pi_10^6 Frontier Audit

This package performs a read-only inspection of the existing Toda (5.9) source-backed specialization, the generic EHP zero-group proof branch, and the actual public group search for n=6, k=4.

It does not install a mathematical rule, register a new GIVEN, change production files, or assert a completed proof. It checks reviewed Git blobs rather than insisting on a fixed HEAD, so audit-only commits are permitted.

From the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r14_pi106_frontier_audit\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r14_pi106_frontier_audit\run.ps1
```

The detailed report is written to `%TEMP%\EHP_Phase175_R4R14_pi106_frontier.json`. Full-suite pytest is deliberately excluded.

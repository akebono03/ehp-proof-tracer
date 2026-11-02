# Phase 173 R3: Portable Read-Only Audit

This package audits the typed root proposals of the two priority groups without changing production source code or promoting registered DB goals to proofs.

It addresses two previous execution failures: a hard-coded Git commit guard and the R1 audit path belonging to another Windows user profile.

From the repository root, unpack the ZIP and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r3_portable\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r3_portable\run.ps1'
```

The run checks the reviewed baseline lineage and exact source blob hashes. Only newly added files under `phase173_*` may have been committed since the baseline. If production source files have been modified, the audit refuses to run until those changes are reviewed.

Reports are written to `%LOCALAPPDATA%\EHPProofTracerRecovery\phase173_r3_portable`. A missing local R1 report is explicitly marked as unavailable, not silently treated as evidence. The full pytest suite is not run.

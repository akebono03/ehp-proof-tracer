# Phase 174 R56R1 — Audit report path correction

This is a narrow, source-guarded repair of the R56 report-directory Path expression. It changes only the untracked `phase174_r3_r7_r56_cyclic_generator_bridge/audit.py`. It does not alter proof rules, the production search, math sources, citations, or renderers.

Unpack the ZIP at the repository root. From PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r56r1_audit_path_fix\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r56r1_audit_path_fix\run.ps1"
```

The runner verifies the reviewed R56 installation and the full SHA-256 of the original audit module, runs targeted report-path regression tests, and reruns the unchanged mathematical certification. It does not rerun the entire pytest suite. If the original file has been modified unexpectedly, the installer refuses to overwrite it.

A passing end-to-end run prints `PASS_R56R1_REPORT_PATH_AND_R56_PUBLIC_AUDIT`.

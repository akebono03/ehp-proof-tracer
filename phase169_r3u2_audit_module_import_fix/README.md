# Phase 169 R3U2 — Audit Module Import Repair

R3U2 restores the same mathematical production function and corresponding
R3I compatibility tests from R3U1. It changes only the way the final audit
is launched, so repository-root imports work in Windows PowerShell.

From the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r3u2_audit_module_import_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r3u2_audit_module_import_fix\run.ps1"
```

`run.ps1` calls the final audit via
`python -B -m phase169_r3u2_audit_module_import_fix.audit` with the
repository root as the working directory. This places the root on Python's
module search path without altering `PYTHONPATH`.

The focused test count is 39 (5 new R3U tests; three sets of 8 R3I tests;
10 prior 1-stem regression tests). These passed in the previous R3U1 user
run; the final audit was not reached due to the launch-path error.

If any check fails, files modified by this package are restored.
The full test suite is **not** run in this phase step.

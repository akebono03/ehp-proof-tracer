# Phase 165 R5-R10 — Legacy Narrative Dependency Ownership

This package is a **read-only audit**. It classifies static uses of four historical Narrative modules as application, audit scripts, or tests. No application source file is changed. No full pytest suite is run.

Run from the repository root in PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase165_renderer_r5_r10_dependency_triage.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_renderer_r5_r10_dependency_triage\run.ps1"
```

Review `audit_output/audit.json` and `audit_output/review.md`. Counts are import/call sites, not a runtime execution profile. External API use and dynamic imports are not ruled out. Historical Phase 162 fixture regression remains unresolved.

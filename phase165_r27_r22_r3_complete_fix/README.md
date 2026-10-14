# Phase 165 R27-R22-R3: Complete Function Repair

This package repairs an R27-R22 Group Query migration that has the modern search import but still does not convert a verified group-structure conclusion to `FOUND`. The installer compares the entire syntax tree of `build_standard_web_group_query_view()` and replaces its body when necessary, while preserving unrelated definitions and import ordering. It also repairs missing imports, removes obsolete imports, and writes a backup before changes. Only the targeted six tests run; the full suite is not run.

Run from the repository root in PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase165_r27_r22_r3_complete_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r27_r22_r3_complete_fix\run.ps1"
```

A COMPLETE result can produce `FOUND` only when the conclusion is an equality for the requested group, and the result's group structure is KNOWN. Otherwise the existing API returns `NOT_FOUND` without claiming a proof. Any partial proof is displayed via the existing Group Proof interface.

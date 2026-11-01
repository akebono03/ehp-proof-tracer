# Phase 173 R3 – Existing report frontier readout

This is a read-only formatter for the **already created** `phase173_r3_manual/audit.json` report. It makes no mathematical inference and never starts proof search, changes production source files, or edits official project documentation.

From the repository root after extracting the ZIP:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r3_frontier_readout\run.ps1'
```

The runner executes only the included focused pytest and prints the four candidate roots and their immediate proof obligations. It does not execute the complete test suite. The report is validated as originating at commit `10f77860a5631d363d606e76b8c1f12ee6c500d5`. Its stored source observations are not proof certificates.

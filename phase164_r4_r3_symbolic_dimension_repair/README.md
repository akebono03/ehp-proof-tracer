# Phase 164 R4-R3 symbolic-dimension repair

This minimal repair handles the symbolic n-family in the existing Toda group model. It does not alter production inference, grant citation eligibility, or perform mathematical certification. The runner replaces the previous R4-R3 audit module and focused tests, executes only targeted pytest, and regenerates the R4-R3 report.

Run from the repository root using PowerShell after extracting this archive into that root:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase164_r4_r3_symbolic_dimension_repair\run.ps1"
```

The full pytest suite is deliberately not executed.

# Phase 165 R6-2 R4-A-R5: Read-Only Failure Diagnostics

Run `run.ps1` in PowerShell from the repository root after installing R4-A-R4.
Requires Python 3.10+ and pytest. No production files are modified.
Outputs `reports/failure_reasons.json` and `reports/failure_reasons.md`.

The audit samples the registered typed assertion contents (the same selection as R4-A-R4), records conclusion mismatches and unresolved premise variables, and statically inspects the pi4^3 adapter and shared provider. These are diagnostic observations, not proof completion certifications. The source imports and calls existing repository factories in the same manner as R4-A-R4.

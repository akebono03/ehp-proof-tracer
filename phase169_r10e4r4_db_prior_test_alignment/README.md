# Phase 169 R10E4R4 — Focused parser and policy-test alignment

This package repairs the R10E4R2 CSV row scanner and updates four historical
R10E1/R10E2 tests to distinguish an unscreened literature source from a
separately admitted prior database result. No group structure or mathematical
inference rule is introduced.

Extract the ZIP at the repository root and execute:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase169_r10e4r4_db_prior_test_alignment\run.ps1"
```

Prerequisites: Phase 169 R10E4 plus the R10E4R1 historical test repair and
R10E4R3 PowerShell runner repair, on reviewed develop commit
`7a687a58443d1cfe40ba03923dd9be60fa462788`.

The runner backs up its inputs, overlays the corrected R10E4R2 function
payload, runs the established focused test/audit workflow and five new
scanner checks, and restores files if any step fails. No full pytest suite
is run. DB records remain adopted hypotheses, not Toda literature theorems.

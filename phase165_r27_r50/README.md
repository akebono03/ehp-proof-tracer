# Phase 165 R27-R50: Typed Group Calculation Entry

This installer **adds** `build_toda_partial_result(query)` and `build_standard_toda_partial_result(n, k)` to `toda_calculation_facade.py`. Both delegate to the canonical registry-backed group search and return its `PartialProofResult` unchanged.

Existing `build_toda_report` and `build_standard_toda_report` remain intact for compatibility. The four legacy repository modules are **not** removed in this step. They cannot safely be removed while `TodaGroupResult` requires `ProofRepositoryEntry` and legacy report consumers remain.

The installer creates `phase165_r27_r50_backup` and `phase165_r27_r50_audit.json`, and executes focused tests only. The tests cover installation and actual delegation using an isolated search stub; they do **not** certify any homotopy group or run the entire repository suite.

Run from the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase165_r27_r50.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r27_r50\run.ps1"
```

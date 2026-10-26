# Phase 169 R3J1 — Focused pytest import isolation

This is an **AUDIT_ONLY** package. It modifies no production code, existing tests, or project documents.

## Root cause

The repository contains both `phase165_r14_r5_ehp_connection.py` (the canonical, upgraded module) and `phase165_r14_r5_ehp_connection/phase165_r14_r5_ehp_connection.py` (an older copy). When the legacy adapter test and the narrative audit test run together, pytest adds the legacy test directory to the module import search path and selects the old copy. It then raises `ImportError` for the R3F/R3I terminal functions. The normal Web path and the earlier R3I2 proof closure do not use that shadow path.

## Solution

Run existing legacy adapter tests in a separate pytest process, then start a fresh pytest process for the unchanged R3J narrative audit and two new import-route regression tests. Verify the canonical module path with the package preflight module before collection (avoiding PowerShell `-c` quoting problems). This preserves the prior evidence and never changes `PYTHONPATH` globally.

From the repository root in Windows PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r3j1_narrative_import_isolation.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r3j1_narrative_import_isolation\run.ps1"
```

Expected success markers: `R3J1_ROOT_EHP_MODULE_OK=True`, `R3J1_EHP_ADAPTER_PYTEST_EXIT_CODE=0`, `R3J1_NARRATIVE_PYTEST_EXIT_CODE=0`, `R3J1_AUDIT_EXIT_CODE=0`, and `R3J1_COMPLETE`.

The report files are `output/pi5_3_current.md` and `output/pi5_3_narrative_audit.json` inside this package. The narrative audit is descriptive and does not modify the renderer or certify new mathematics. Full pytest remains deferred until the end of Phase 169.

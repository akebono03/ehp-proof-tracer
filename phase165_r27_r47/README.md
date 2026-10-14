# Phase 165 R27-R47: Conservative Legacy Dependency Pruning

This package audits active top-level Python imports, preserves every reachable legacy `repository_*` module, and removes only unreachable legacy modules. Deleted source files are backed up before removal. A JSON audit records active legacy imports and the remaining migration boundaries in `toda_calculation.py` and `standard_production_applicability_catalog.py`.

This step does **not** claim that the remaining group calculation or applicability catalog has been migrated. It does not execute the full test suite.

Run from the project root using `powershell -ExecutionPolicy Bypass -File .\phase165_r27_r47\run.ps1`.

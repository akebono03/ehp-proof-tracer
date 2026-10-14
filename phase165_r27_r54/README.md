# Phase 165 R27-R54 — Legacy Group Calculation Dependency Audit

This package performs a read-only dependency audit of the four remaining `repository_*` modules. It writes `phase165_r27_r54_audit.json` to the project root and runs seven focused tests.

The audit uses Python AST imports, including imports in functions and literal dynamic imports. It does **not** delete production files or claim that the legacy calculation and report APIs have been replaced. It distinguishes direct dependents from modules with no detected static importers; indirect or nonliteral dynamic imports may still exist.

## Run on Windows PowerShell

```powershell
Expand-Archive -Path "$HOME\Downloads\phase165_r27_r54.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r27_r54\run.ps1"
```

Only targeted tests are run. Full pytest remains reserved for Phase 165 closure.

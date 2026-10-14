# Phase 165 R27-R48

This installer replaces only the base rule collection inside `standard_production_applicability_catalog.py` with shared typed inference rule discovery. Historical classification wrappers are retained. It does not delete or migrate `toda_calculation.py`, and no new proof is certified by catalog membership.

Run from the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase165_r27_r48.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r27_r48\run.ps1"
```

The installer saves the original catalog in `phase165_r27_r48_backup` and writes `phase165_r27_r48_audit.json`. Only targeted installer tests run; no full pytest.

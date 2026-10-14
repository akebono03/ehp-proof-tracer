# Phase 165 R27-R48-R1 — Catalog Installer Fix

This patch updates the base `build_standard_production_applicability_catalog()` function while preserving the existing classification-wrapper chain. It accepts previously modified base function bodies, checks for references to legacy imports outside that function, saves a backup, and runs only targeted installer tests.

Run from the project root in PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase165_r27_r48_r1.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r27_r48_r1\run.ps1"
```

No full pytest is run. Group calculation remains unchanged. This does not certify mathematical completeness of the catalog.

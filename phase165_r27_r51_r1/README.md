# Phase 165 R27-R51-R1 installer correction

This package preserves an already migrated typed Web Group Query implementation. It updates the legacy query entry only when the old `build_standard_toda_report` call is actually present. It will not silently rewrite an unknown implementation.

Changed target: `web_group_query.py`, function `build_standard_web_group_query_view` only when necessary. Imports from the legacy report and renderer are removed only for the legacy implementation. The `WebGroupQueryView` class remains unchanged.

Run from the repository root in PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase165_r27_r51_r1.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r27_r51_r1\run.ps1"
```

The package performs targeted tests only. Unknown implementations stop safely and are not overwritten. Backups and audit output are written beside the package.

# Phase 165 R4 Interrupted Rollback Recovery

This package restores the pre-R4 project source files and legacy import compatibility package from the original `.phase165_renderer_r4_backup`. It never deletes that backup.

Run from the repository root using PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase165_renderer_r4_recovery_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_renderer_r4_recovery_fix\run.ps1"
```

The package verifies that the entire backup manifest is available *before* modifying any source. Originals are copied using per-file staged replacement, making reruns safe. It runs narrowly targeted tests and compares the original completed and incomplete Narrative outputs with the saved R4 baseline. It does not run the full suite. Do not rerun the old R4 installer.

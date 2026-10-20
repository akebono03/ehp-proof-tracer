# Phase 166 R3-Q Recovery

This package reverses only the failed R3-Q modification to `search_group_from_registered_goal()` in `phase165_r55_nk_only_goal.py`. It reads the exact backup created at `20261020T103615Z` and refuses to proceed if the backup or current function does not match the expected state. It preserves other functions and all R3-P reference order data. The prior current file is backed up separately.

From the project root in Windows PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase166_r3q_recovery.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase166_r3q_recovery\run.ps1"
```

The installer creates `phase166_r3q_recovery_results/report.json` and `RESTORED_FUNCTION.py.txt` containing the complete restored function. It then runs the six existing R3-D pi3^2 regression tests. The full pytest suite is not run. Passing tests restore the pre-R3-Q behavior but **do not complete R3-Q**.

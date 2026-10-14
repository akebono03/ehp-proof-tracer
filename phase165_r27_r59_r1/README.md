# Phase 165 R27-R59-R1 — Legacy Calculation Retirement Repair

This package repairs R59's all-or-nothing gate by separating historical audit scripts and legacy-only tests from active production code. It preserves every retired file in a verified ZIP backup before removal.

## Modified files and functions

- `toda_calculation_facade.py`: removes the full legacy `build_toda_report()` and `build_standard_toda_report()` functions and now-unused imports, while retaining the existing typed partial-result functions unchanged.
- Retires `toda_calculation.py`, `toda_calculation_report.py`, and four legacy `repository_*` modules.
- Archives legacy-only tests and standalone historical audit scripts when safe.
- Installer functions `plan()` and `apply()` are updated to identify historical scripts, scan consumers and recursively archive dependent tests. Installer tests are expanded.

## Safety

Files are only removed when there are no remaining references outside the approved retirement set. The installer refuses to remove audit scripts still imported by active modules. All affected files are stored in `phase165_r27_r59_r1_retirement_backup.zip` before changes. If any blockers remain, it produces `phase165_r27_r59_r1_audit.json` with `status=BLOCKED` and makes no source changes. Dynamic imports assembled from runtime strings may require manual review.

## Run

From your repository root in PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase165_r27_r59_r1.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r27_r59_r1\run.ps1"
```

Only installer-targeted pytest tests run; full pytest is deferred to the end of Phase 165. Passing these targeted tests is not certification that mathematical proofs are correct.

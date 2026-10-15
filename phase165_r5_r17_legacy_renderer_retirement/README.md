# Phase 165 R5-R17: Legacy Renderer Retirement

Run `run.ps1` from the extracted package. The script verifies the shared EHP-input module and scans application/root tests for imports of four retired renderer modules. On an unexpected active import, it aborts without deleting files. Otherwise it backs up and removes four legacy renderer modules and five renderer-specific historical test modules. It then runs a focused common Renderer regression test and restores the deleted files if that check fails. Full pytest is intentionally not run.

The backup directory is `.phase165_r5_r17_removed_backup`. `restore.py` can restore removed files while retaining the backup. Historical phase packages and archived audit scripts are not deleted. See `AUDIT.md` for the precise boundary.

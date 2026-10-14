# Phase 165 R27-R40 — Legacy Generator helper retirement

Removes only unreferenced private legacy Web adapter helper definitions and now-unused legacy imports. It then recomputes the conservative static dependency graph and backs up and deletes orphaned `repository_*.py` modules. Public views and typed-search entry functions remain untouched. A mismatched signature or surviving reference causes the installer to fail closed. It does not run full pytest.

From the project root, expand the archive and run `powershell -ExecutionPolicy Bypass -File .\phase165_r27_r40\run.ps1`.

Report: `phase165_r27_r40_audit.json`; backups: `phase165_r27_r40_backup`.

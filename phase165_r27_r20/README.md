# Phase 165 R27-R20: Guarded Legacy Backup Removal

This package removes only explicitly named obsolete root-level Python backup files, after checking for root-level references. Each removed file is preserved byte-for-byte under `removed_files_backup/`. It never removes active `ProofRepository`, Bootstrap, inference rules, typed statement registries, or application entry points.

Run from the repository root using `powershell -ExecutionPolicy Bypass -File .\phase165_r27_r20\run.ps1`.

The script writes `audit_report.json` with `REMOVED_WITH_BACKUP`, `ABSENT`, and blocking statuses. It is safe to run repeatedly. Only three targeted tests run; the full suite is reserved for the end of Phase 165.

The active Bootstrap cannot yet be safely removed: public and production consumers still exist. Migrating those consumers to the new proof engine is a prerequisite, not part of this package.

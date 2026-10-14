# Phase 165 R27-R26

This package retires the old standard production applicability catalog entry and removes `standard_production_repository.py` and `toda_prop515_upper_bootstrap.py` **only when no active top-level Python module imports either module**. Archived scripts, tests, and backups are not treated as active production imports. All removed files and changed source are saved to `removed_files_backup` before deletion.

The existing typed statement registry, shared rule provider, and common Backward Search are unchanged. This migration intentionally changes the retired applicability catalog API to raise `RuntimeError`; the explicit repository-dependent APIs remain untouched. Existing historical tests may need migration and are not claimed to pass.

Run `run.ps1` from the extracted directory. The installer aborts without modifying production files if any active top-level source import remains. The operation is idempotent once the catalog is migrated; a follow-on R26 repair might still be needed if the local checkout differs from the GitHub snapshot.

Only targeted tests run here. The full suite must wait until the end of Phase 165.

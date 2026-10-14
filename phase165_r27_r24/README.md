# Phase 165 R27-R24

Retire the legacy standard calculation entry without manufacturing empty mathematical results. `build_toda_report(repository,n,k)` remains available for explicit repository callers, while `build_standard_toda_report(n,k)` now raises a clear migration error rather than rebuilding the legacy bootstrap. Web and CLI group query entrypoints were migrated in R27-R22 and R27-R23.

Run `run.ps1` from the extracted package. The patch is guarded, idempotent, and backs up the original source before writing. Tests are targeted only. This does not delete the standard repository/bootstrap modules, and does not prove that every historical test passes.

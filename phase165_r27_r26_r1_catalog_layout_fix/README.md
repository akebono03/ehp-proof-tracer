# Phase 165 R27-R26-R1

Fix the installer assumption that `build_standard_production_applicability_catalog()` must still exist in the local checkout. An already-removed entry with no remaining old builder import or call is accepted without changing the catalog. An ambiguous old import or a use outside the standard function still blocks deployment.

The original safety guard is retained: removal of `standard_production_repository.py` and `toda_prop515_upper_bootstrap.py` is blocked until no active root-level Python module imports them. On such a failure, the installer produces `audit_report.json` and makes no production changes. The explicit-repository APIs and shared typed search are preserved.

Run the included PowerShell `run.ps1`. Only targeted tests are run. A full pytest run is deferred until the end of Phase 165.

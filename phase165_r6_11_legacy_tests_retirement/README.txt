Phase 165 R6-11: retire the 13 Phase 49 / Phase 56 / Phase 55 named legacy test files from the R6-10 audit.

NO legacy Probe source is removed or edited in this step, because active dependency boundaries are not yet resolved.
R6-11 does NOT claim the previous 69 test cases are exactly covered by these 13 files.

Run from the repository root with PowerShell:
powershell -ExecutionPolicy Bypass -File .\phase165_r6_11_legacy_tests_retirement\run.ps1

Preflight parses Python files and refuses to move any file on parse errors or imports of candidate test modules outside the batch.
On successful preflight: copies candidates to phase165_r6_audit_results/r6_11_legacy_tests_retirement/backup_<UTC>/tests/ with SHA256 manifest, verifies backups, then removes the original test files.
No full pytest is performed. No source, production, math or rule files are edited.
Review report.json after running; a BLOCKED status does not remove any test files.

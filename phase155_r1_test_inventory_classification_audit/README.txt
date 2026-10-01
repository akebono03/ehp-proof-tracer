Phase 155-R1 — Test inventory / classification audit

Scope
-----
- Static audit only.
- Production code is not modified.
- Existing repository tests are not modified or deleted.
- The repository-wide pytest suite is NOT executed.
- Phase numbers alone are never used to mark tests historical.

Generated outputs
-----------------
phase155_r1_audit_output/phase155_r1_test_inventory.csv
phase155_r1_audit_output/phase155_r1_file_inventory.csv
phase155_r1_audit_output/phase155_r1_duplicate_groups.csv
phase155_r1_audit_output/phase155_r1_summary.md
phase155_r1_audit_output/phase155_r1_metadata.json

Run from PowerShell after extracting the package into the repository root:

powershell -ExecutionPolicy Bypass -File ".\phase155_r1_test_inventory_classification_audit\run_phase155_r1_test_inventory_classification_audit.ps1"

This R1 package does not make deletion decisions. R2 should use the inventory to inspect stale expectations; R3 should review duplicate/superseded candidates.

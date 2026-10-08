Phase 161 Search Boundary Audit (read-only)
Run from the repository root:
  powershell -ExecutionPolicy Bypass -File ".\phase161_search_boundary_audit\run_phase161_search_boundary.ps1"

This does not modify the repository source or tests and does not run pytest.
It constructs a diagnostic catalog from Phase 59's known seven rules and six seeds.
It checks seven intermediate goals individually, reports bounded-search status,
and compares against the depth of their previously derived forward proof graphs.
The catalog is NOT the production catalog and this is NOT a goal-only proof discovery test.
Output: phase161_search_boundary_audit.json

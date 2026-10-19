# Phase 165 R6 consolidated failure triage

This is a read-only audit tool, **not** a retirement or migration installer.

Unpack into the repository root and execute `phase165_r6_consolidated_audit/run.ps1`.
The script reads the 490-node historical failure manifest bundled with this
package, scans local test files, and produces three reports in
`phase165_r6_audit_results/consolidated_triage/`:

- `summary.json`: counts by triage category.
- `failed_nodes_triage.csv`: one row per failed test.
- `failed_files_triage.csv`: one row per affected test source file, plus SHA256.

`LEGACY_CANDIDATE` does not authorize removing a test: replacement contract
coverage must be audited first. No tests are executed and no files are moved,
modified, or deleted.

# Phase 165 R6 Safe Test Cleanup

This package makes one narrowly scoped deletion: `tests/test_phase164_r7_statement_resolution.phase164_r7_r1_backup.py`.

The backup-named file is an obsolete duplicate fixture snapshot, while the active `tests/test_phase164_r7_statement_resolution.py` remains untouched. The command refuses to delete if the active file is missing, if the expected signature differs, or if an already saved backup could be overwritten. Before deletion, it copies the file to `phase165_r6_audit_results/safe_test_cleanup/` and checks matching SHA-256 hashes.

Run `run.ps1` from the repository root, then `rollback.ps1` to restore the backup if necessary. The runner invokes only the retained active test; it does not run the whole suite. No production implementation, renderer, probe, or other test is changed.

This is a first, conservative cleanup step. The 259 transitive dependency failures are not candidates for blanket deletion without verifying coverage of mathematical and presentation contracts.

# Phase 165 R57-R5 — Backup-only renderer reference cleanup

This patch removes one obsolete Phase 159 public narrative helper **only if** there are no references to it in any other current root-level production Python module or current tests. References from backup files are reported but do not block removal. The patch does not delete backup files.

The live public renderer entry point, its retained alias, stable finite-cyclic transport renderer, mathematical statement renderers, ProofSteps, and search logic are unchanged. This is a dead-code cleanup, not a replacement for the remaining live specialized-renderer branches.

The installer writes `phase165_r57_r5_reference_audit.json` to the repository root, saves a backup before editing, and rejects deletion when active references are present. It is idempotent. No new group-specific rendering text is introduced.

To apply: unzip into the repository root and invoke `phase165_r57_r5_backup_reference_cleanup/run.ps1`. The runner executes five targeted pytest modules, never the full test suite.

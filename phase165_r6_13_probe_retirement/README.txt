Phase 165 R6-13: retirement of legacy Phase49 and Phase56 Probes.
Current code only, no old mathematical rules or generic search modified.
The script refuses changes if another active module imports either legacy Probe.
Backups with SHA-256 manifest are created before removal.
Phase58's print_separator becomes a local helper with unchanged output.
A failed import smoke test restores all modified files from the backup.
Only package tests are run. Full pytest is deferred until phase close.

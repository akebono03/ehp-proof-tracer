# Phase 165 R6 — dependency-closed historical test cleanup

Reads the latest pytest collection log, checks the count against the actual error headers, and identifies legacy Phase <=129 test files that failed due to removed repository / Phase 50 probe machinery. It retains every file referenced by a surviving test (including current Phase tests) and removes only a dependency-closed candidate set after SHA-256 verified backups. A new `--collect-only` log is produced and parsed independently, without running test bodies. No production source, adapter, or renderer is added or modified. Deletion decisions are not mathematical certification; review the report and restore a session if needed. The baseline must contain a matching pytest error count. The script does not promise elimination of all collection errors.

Run `run.ps1` from the repository root. Restore by passing the session directory to `rollback.ps1 -Session PATH`.

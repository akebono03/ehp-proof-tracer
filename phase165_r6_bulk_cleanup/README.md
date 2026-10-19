# Phase 165 R6 conservative bulk cleanup

This package uses the corrected 380-error recollection report and its log. It removes only failing Phase <130 leaf tests with a directly imported missing `repository_*` implementation module. All deletions have verified SHA-256 backups and a per-file decision record. Phase 130+ and tests imported by any other active test remain unchanged. It then runs pytest collection only, not full tests. Use rollback.ps1 with the saved session directory to restore files. Does not alter production code or reinstall removed APIs.

# Phase 165 R57-R22: Backward Search Connection Audit

This package performs **read-only** source inspection and a limited existing-adapter frontier probe. It does not install or modify production code and does not run the full test suite.

Extract this directory into the repository root, then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase165_r57_r22_connection_audit\run.ps1
```

The audit creates `audit_results.json` inside its own directory, containing static checks and, where imports work, five existing-adapter goal probes. The dynamic probe tests adapter proposals, **not** full search reachability after removing the adapter. This distinction must be resolved in the following phases before deleting the adapter.

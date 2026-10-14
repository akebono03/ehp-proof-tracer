# Phase 165 R27-R39: Shared Toda Conclusion Renderer

Extract the repository-independent LaTeX conclusion renderer to `toda_conclusion_latex_renderer.py`. Update twelve production consumers' imports only. No group proof functions or legacy compatibility types are deleted in this step; these remain available until all runtime consumers have migrated. Missing optional root modules are skipped and recorded in the audit.

## Installation

Extract the ZIP into the project root. In PowerShell from the project root run:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase165_r27_r39\run.ps1
```

Backups: `phase165_r27_r39_backup`. Audit: `phase165_r27_r39_audit.json`.

## Tests

Only six installer/contract checks are run; no full pytest. The next step can migrate generator-specific presentation types and then repeat repository reachability auditing.

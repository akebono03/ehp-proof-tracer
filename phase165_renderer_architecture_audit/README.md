# Phase 165 Renderer Architecture Audit

This package performs a read-only AST inspection of the current repository, focusing on the rendering pipeline from Web view to presentation, generic narratives, reasons, references, and normalization. It reports same-file redefinitions, calls, feature locations, and potential test entrypoints.

Run in the repository root after extracting the ZIP:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase165_renderer_architecture_audit\run.ps1
```

Outputs: `phase165_renderer_architecture_audit_output/report.md`, `audit.json`.

No production files are modified, and pytest is not run. The tool does not assert runtime reachability or mathematical validity from static data.

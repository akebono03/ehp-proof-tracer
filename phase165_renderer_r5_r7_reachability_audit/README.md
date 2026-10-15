# Phase 165 R5-R7 — Narrative Route Reachability Audit

This is a **read-only** static audit of the Group Proof entry modules and three specialized or historical narrative functions.

Run in PowerShell from the repository directory after extracting this package:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase165_renderer_r5_r7_reachability_audit\run.ps1"
```

Outputs: `audit_output/audit.json` and `audit_output/review.md`.

The audit inspects active top-level Python modules; it excludes explicitly suffixed historical `.phase` snapshots, audit scripts, and probe scripts. An import chain is conservative evidence of possible access, **not** proof of a function being invoked. Dynamic registration, reflection, and CLI surfaces are not certified.

No application source files are modified. No project-wide pytest is run. The unresolved six historical Phase 162 fixture failures are not reclassified or hidden.

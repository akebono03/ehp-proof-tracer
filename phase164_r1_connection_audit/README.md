# Phase 164 R1 — Read-only Connection Audit

This package audits the installed EHP Proof Tracer repository without changing application source code, existing tests, or documentation. It inventories the registry, bridge, source archive, Phase 161 reconstruction, provenance validation, and Phase 162 presentation adapter. It runs only explicitly selected focused regression tests that exist locally.

From the repository root, extract this directory and run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase164_r1_connection_audit\run.ps1"
```

The audit writes `phase164_r1_output/report.json` and `report.md`. It does not run the entire pytest suite. The output is an implementation inventory and does not certify mathematical statements or grant citation eligibility.

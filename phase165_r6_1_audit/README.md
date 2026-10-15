# Phase 165 R6-1 — Backward Search connection audit

This package performs a **read-only** audit of the repository's top-level Python search modules. It flags potential per-group branching and verifies the known simultaneous links from the shared expansion provider to the dedicated pi4_3 adapter and generic discovery. It does **not** remove files, install patches, certify mathematical rules or execute the entire test suite.

Unzip into the repository root and run `powershell -ExecutionPolicy Bypass -File .\phase165_r6_1_audit\run.ps1`.

The report is written to `phase165_r6_1_audit/audit_report.json`. Review all candidates; false positives are expected. R6-2 is responsible for generic inverse rule applicability, not this package.

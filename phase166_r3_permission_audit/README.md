# Phase 166 R3 — Proof-Permission Boundary Audit

This package performs a read-only audit of the current production registry, literature citation gate, and recursive-search reference lookup modes.

Extract the ZIP at the project root and run `powershell -ExecutionPolicy Bypass -File .\phase166_r3_permission_audit\run.ps1`.

The audit does not certify mathematical content, grant citation rights, create `ProofStep` objects, or edit production code. It intentionally records whether different lookup modes apply different conditions. A successful audit is **not** permission to use legacy source metadata as a proof premise.

Outputs are written to `results/summary.json`. The script runs only targeted pytest tests. Full pytest is reserved for the Phase boundary.

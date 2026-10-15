# Phase 165 R5-R12 — Legacy Narrative Retirement Gate

This is a **read-only, function-level dependency audit**. It validates the local Phase R5-R11 EHP-leaf decoupling, inventories static import and call references to the legacy Phase 162 Narrative functions, and records provisional retirement decisions. It does **not** delete or rewrite production source, does not certify mathematical correctness, and does not run the full test suite.

Run `run.ps1` from the extracted directory on Windows. Outputs are `audit_output/audit.json` and `audit_output/review.md`.

A reported retirement candidate is not authorization to remove a public Python API: external consumers and dynamic imports may exist. Existing Phase 162 fixture regressions remain unresolved.

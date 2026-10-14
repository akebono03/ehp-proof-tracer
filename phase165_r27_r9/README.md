# Phase 165 R27-R9: Legacy Builder Dependency Inventory

This package performs a read-only function-level audit. It does not remove or modify production code. Run `run.ps1` from the repository root. `audit_report.json` records definitions, imports, calls, and relevant root-level tests. It intentionally excludes protected typed-statement registry and prover files from deletion candidates.

The audit is not authorization to delete a file. In particular, `web_group_proof.py` contains Web view structures and helpers still imported by the common partial-proof adapter.

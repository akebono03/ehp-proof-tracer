# Phase 168 R3-22: Read-only Gap Audit (Import Fix)

This package audits the frozen narrative baselines against the active model-backed renderer. It does not change the application's source files or tests.

The corrected `run.ps1` invokes the audit as a Python module from the repository root, with the repository root explicitly included in `PYTHONPATH`.

Extract the package at the repository root and run `phase168_r3_22_gap_audit_importfix/run.ps1`. Outputs are written to `output/` inside the package. No full pytest is run.

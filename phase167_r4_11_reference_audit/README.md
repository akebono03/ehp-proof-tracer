# Phase 167 R4-11 Reference Usage Audit

This package is read-only. It does not modify production code or run the full test suite.

Run `run.ps1` from the repository root in PowerShell. The script generates `audit_report.json`, capturing the proof-step reference relationships before and after the reference linking function and the final web output for selected `(n, k)` cases. It verifies that the Proposition 4.2 EHP sequence is displayed once in the proof rather than as a reference in the `pi_4^3` narrative, and that both Toda (5.1) specializations retain their citations.

Other cases are reported for review, not declared correct automatically. Any exception or regression check failure exits nonzero.

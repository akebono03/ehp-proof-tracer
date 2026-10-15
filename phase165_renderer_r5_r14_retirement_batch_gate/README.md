# Phase 165 R5-R14 — Legacy Narrative Retirement Gate

This package performs read-only, function-level dependency inspection of historical Phase 162 Narrative entrypoints and two specialized renderers.

## Installation and execution

Extract this ZIP into the repository root and execute `run.ps1` using PowerShell.

The script runs only its own focused pytest suite. It does not run the full repository test suite and does not modify application files.

Results are written to `audit_output/audit.json` and `audit_output/review.md`.

The next step, R5-R15, may change code only after reviewing this report and verifying existing public interfaces and focused regression tests.

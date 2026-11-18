# Phase 175 R4R12R1R2 — Historical Prior-Report Fixture Fix

This small overlay fixes a test fixture that incorrectly used the current R4R12 HEAD as the historical R4R11 audit-report HEAD. The production `validate_prior()` function correctly requires the earlier HEAD and must not be relaxed.

Extract the ZIP into the repository root on the reviewed `develop` HEAD. Run `run.ps1 -DryRun`, then `run.ps1` to patch the fixture and execute the existing R4R12 focused audit. The patch is guarded, idempotent and preserves CRLF/LF. It changes only the untracked R4R12 `tests/test_audit.py` fixture; it does not alter inference rules, production source code or prior audit reports.

The full R4R12 focused pytest suite runs in the original R4R12 runner. The project-wide pytest suite is not run.

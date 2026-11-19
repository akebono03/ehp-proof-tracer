# Phase 175 R4R14R1 — Pytest Collection Fix

This is a read-only runner correction for the existing Phase 175 R4R14 audit. It fixes pytest's import-file mismatch when two test directories contain a `test_rule.py` by setting `--import-mode=importlib`.

It does not alter the original audit, production modules, test definitions, source citations, or mathematical rules. The original `phase175_r4r14_pi106_frontier_audit` package must already be present at the repository root.

From the repository root, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r14r1_pytest_collection_fix\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r14r1_pytest_collection_fix\run.ps1
```

The underlying audit report is `%TEMP%\EHP_Phase175_R4R14_pi106_frontier.json`. The full test suite is deliberately not run.

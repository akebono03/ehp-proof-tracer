# Phase 175 R13R8R8R1 — Read-only Closeout Audit

This is the HEAD-guard correction of the R13R8R8 closeout package. It does not modify production sources, proof rules, or GIVEN statements.

## Repository requirement

Use the `develop` branch. The known reviewed baseline commit is `b5a0b13884f6f0af527034d8c8bcd47b90c7cc97`. The local HEAD can be a descendant of that baseline; an exact HEAD match is **not** required. The audit verifies Git ancestry and exact Git blob equality for both relevant production files in HEAD, the index, and the working tree. If either file changes, the audit fails closed.

## Run

Unzip into the repository root and execute:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r13r8r8r1_closeout_head_guard_fix\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r13r8r8r1_closeout_head_guard_fix\run.ps1
```

The full run checks the three completed public proof views and R3/R7 narrative citations, then runs the 13 existing focused tests without the pytest cache provider. No full pytest suite or production code modification is performed. The report is written in the system temporary directory. The results do not guarantee all possible future statement families.

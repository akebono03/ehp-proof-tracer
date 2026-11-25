# Phase 176 Closeout R3 — Recover document publication

This package recovers the five full documents after R2 passed all 3546 active tests in 41.33 seconds but failed to publish the documents with a Windows PermissionError. It never runs the full suite again. It does not modify mathematical code, historical gates, test assertions or previous reports.

The reviewed source HEAD is `7b4e071b735d8c309c2155c04c96869e7e774bdb`. Keep the existing R2 package and all previous evidence. R3 verifies the exact R2 stdout/stderr digests, report, attempt, preflight, public audit, R1 archive and evidence, original document hashes and source scope. Each document must equal its verified original, the R2 edition, or the R3 edition. Unknown edits are rejected. A lock may leave a subset of documents published; a later R3 attempt may continue from these exact known states. No rollback over locked or concurrently edited files is attempted. Do not delete old evidence or reset documents. Close editors and, if appropriate, temporarily pause Dropbox sync before running. Resume sync after the run.

Run from repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_closeout_r3\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_closeout_r3\run.ps1
```

Only the ten focused R3 tests are run. The evidence and complete original/final documents plus ZIP are saved in a new `attempt_*` directory beneath `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_closeout_r3`. `final_report.json` is created only on successful final verification. The full-suite result is reused, not a new run. If the gate fails, inspect the printed traceback/path and the attempt report. If an unexpected tracked or untracked file is reported, review it manually; the package does not delete it. The four historical Phase 174 guards remain unresolved and are not counted as passing.

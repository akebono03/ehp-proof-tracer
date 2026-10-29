# EHP Proof Tracer — Phase 171 R1C-R2: CSV separator repair

This is a narrowly scoped repair of the R1C CSV inventory. The project CSV contains the separator row `3,,,,,,,,,,,,,,` between stem blocks. It is not a registered group and must be skipped. An empty `n` with any other nonempty field still fails closed. No proof-search logic changes.

Phase 171 R1C corrects the audit dimension: **fix `k=3` and vary `n`**, using only explicit `(n, 3)` coordinates in `data/sphere.csv`. This is an audit of the 3-stem `π_(n+3)^n`, not of every `k` for `n=3`. Duplicate CSV generator rows do not increase the number of goals.

This package does not change production code, existing tests, database content, mathematical inference rules, renderer, or formal documentation. It does not make previously unproved groups complete. Workers independently call the current typed-goal proof search and the public Web verification entry point. The audit is pinned to the reviewed Git commit `715b00d67d4b3ff4b34bf87229842d14960ea6bb` and the explicit CSV blob.

## Run from the repository root (Windows PowerShell)

```powershell
Expand-Archive -Path "$HOME\Downloads\phase171_r1c_k3_registered_audit_r2.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r1c_k3_registered_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r1c_k3_registered_audit\run.ps1"
git status -sb
```

Each run executes only the focused tests in this package. `-DryRun` checks Git state and the registered domain without running search workers. Normal mode runs every explicitly registered 3-stem group once (32 distinct `n` values in the reviewed CSV, including two rows for `n=4`). The report is written outside the repository to `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r1c_k3_*` with `audit.json`, `audit.md`, and one log per `n`.

A complete *audit* with unresolved goals returns `AUDIT_COMPLETE_WITH_GAPS`, which is not proof completion. Worker errors are distinguished from unfinished proof search. The full repository pytest suite is reserved for Phase 171 closeout.

The complete replacement audit function, all new tests, full audit source code, test code, and PowerShell runner are reproduced in `CHANGED_CODE_FULL_JA.md`.

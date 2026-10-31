# Phase 172 R6 — Presentation Closeout Gate

This package is a read-only closeout auditor for Phase 172 of EHP Proof Tracer. It **does not patch source files or documents**, does not change the proof tree, and does not introduce mathematics. It verifies the reviewed R5 renderer content before executing any search or test.

The gate checks the public complete narrative for five previously completed groups: pi_3^2, pi_4^3, pi_5^3, pi_6^4 and pi_6^3. For pi_6^3 it verifies the original 50 proof steps, eight references, no open goals, and the R2–R5 display contracts. It executes only the active `tests/` full suite once, after focused tests and all Web checks pass. The Phase 171 baseline was 3,546 passing tests; the current result is independently measured.

## Windows PowerShell

Run from the repository root after extracting `EHP_Phase172_R6_CLOSEOUT_GATE.zip`:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r6_phase_closeout\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r6_phase_closeout\run.ps1" -RunCloseout
git status -sb
git diff --stat
```

`-DryRun` checks GitHub-tracked prerequisites through local Git and checks `origin/develop`; it never runs pytest. `-RunCloseout` runs ten isolated focused pytest groups, five real Web proof queries, and then the complete active `tests/` test suite exactly once.

Reports and logs are written to `%LOCALAPPDATA%\EHPProofTracerRecovery\phase172_r6_*`. `closeout.json` records all gates and the exact log path. No Git commit, checkout, reset, or source patch is performed. The separately reviewed documentation closeout, if needed, follows evidence produced by this run and is not presumed to have passed.

# Phase 173 R4-R1 — Read-only Git status diagnostic

This package diagnoses the preflight error `Tracked files are modified; no automatic clean/reset` without changing the worktree, Git index, or commit history. It reports staged/unstaged tracked paths and whether any file protected by the R4-R1 reviewed-source guard has changed.

Unzip at the repository root and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase173_r4_r1_git_status_diagnostic\run.ps1'
```

`-DryRun` is accepted, but both modes perform the same non-mutating checks. The report is written outside the repository, under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase173_r4_r1_git_status_diagnostic\status.txt`.

A `PASS` means only that the status readout succeeded. It does not approve tracked changes, run a mathematical proof search, or imply R4-R1 completion. Do not reset, checkout, restore, stash, or commit any files as a result of this script alone. No test suite is executed.

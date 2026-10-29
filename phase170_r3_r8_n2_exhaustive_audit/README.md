# Phase 170 R3-R8: exhaustive n=2 DB coverage audit

This is a strictly **read-only audit package**. It makes no changes to the application, tests, documentation, database, or Git index. The repository must be on `develop` in one of two reviewed states: commit `84a9d8ad6110ed82b80bdeb7e9a0c5a361214de0` with only the R3-R7 source modification uncommitted, or commit `f479e0aabdfeefa69ad986e20c0f69ce0efd7bbd` (`170-3-7`) with a clean tracked working tree. Both states must have the identical, SHA-256 verified R3-R7 production source. This package supports the committed state reported on October 29, 2026.

## Windows PowerShell

From the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase170_r3_r8_n2_exhaustive_audit.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r8_n2_exhaustive_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r8_n2_exhaustive_audit\run.ps1"
git status -sb
```

The audit enumerates *explicit* `n=2` rows of `data/sphere.csv`, rather than inventing missing rows using stable-range defaults. Every stem runs in an independent Python process, with a bounded worker timeout. It checks typed target and source DB statements, active proof search, the completed-proof status, and the actual public trust-gated Web narrative. The `k=0` row is reported separately as outside the range of Toda (5.2). Other stems use the project's regular search engine; `k=1,2` may retain established earlier derivations.

The audit does **not** run the full test suite, modify code, declare unresolved cases proven, or transform DB data into unverified mathematical citations.

Results are written beneath `%LOCALAPPDATA%\EHPProofTracerRecovery\phase170_r3_r8_n2_*` as `audit.json`, `audit.md`, and per-stem worker logs. `AUDIT_COMPLETE_WITH_GAPS` is a successful *audit run*, **not** a claim that every homotopy-group proof is complete. Read `domain_gaps` and `rows` before making claims about coverage. The process returns exit code 0 after a complete inspection even when mathematical gaps remain.

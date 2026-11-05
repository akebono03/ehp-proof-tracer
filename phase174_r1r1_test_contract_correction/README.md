# EHP Proof Tracer — Phase 174 R1R1 Focused Test Contract Correction

The first read-only Phase 174 R1 audit completed for three groups but four
legacy tests in `test_phase165_r55_nk_only_goal.py` failed. These tests assumed
an older goal selector and an unrealistically minimal citation registry.
This package updates **only that test file** to match the currently reviewed
production contracts. It does not change the proof search engine, source
registry, mathematical rules, application code, narrative renderer, or any
of the five main documents.

All four failing tests remain part of the focused pytest invocation. The
R1R1 script verifies the remote and local `develop` SHA, original test
content SHA, replacement content SHA, and source guard. `-DryRun` changes
nothing. Normal execution installs the full replacement test and re-runs
the unchanged R1 audit runner, including its focused pytest suite.

The script never calls `git reset`, `git clean`, `git commit`, or `git pull`.
It refuses to overwrite locally edited or staged test content.

Reviewed GitHub HEAD: `cb85913905b2f7452bda2a2c4428e6fe5a3a793a`.

Expected new test blob SHA: `9def7480a529ab5f6c2e344866016cf36330a409`.

## Windows PowerShell

Extract the ZIP at the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r1r1_test_contract_correction\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r1r1_test_contract_correction\run.ps1"
```

The full project-wide pytest remains reserved for the Phase 174 closeout.

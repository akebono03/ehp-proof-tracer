# Phase 170 R3-R9R2 — Exact Toda (7.12) Source Alignment

This package makes a **single, narrowly scoped change** to the untracked
`phase170_r3_r9_toda712_cited_rewrite/source712.py` file prepared by the earlier
R3-R9 package. It replaces only the module-level `CLAUSE` literal with the
actual two-line TeX expression in the adopted Toda Chapter VII source.

It does not alter the `verified_toda712_generator_equality()` function, its
unique-source guard, the typed transport rules, the registry bridge, or existing
repository tests. The original R3-R9 runner is reused after the source literal
is corrected. The original R3-R9 ZIP is **required**; this is not a
reconstruction of the unsuccessful R3-R9 implementation.

## Prerequisites

* Windows PowerShell, Git, Python, pytest
* Repository checkout at `develop` commit
  `fdf60522b6d477209e9d8d67720a63f9863e419c`
* The original `phase170_r3_r9_toda712_cited_rewrite` directory, or its ZIP in
  `Downloads`
* Internet access for the read-only `git ls-remote origin` check
* No pre-existing tracked changes

## Run from the repository root (PowerShell)

```powershell
Expand-Archive `
  -Path "$HOME\Downloads\phase170_r3_r9r2_toda712_source_alignment.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -NoProfile `
  -ExecutionPolicy Bypass `
  -File ".\phase170_r3_r9r2_toda712_source_alignment\run.ps1"

git status -sb
```

Optional `-AuditOnly` checks preconditions without applying any repair.
Optional `-AuditDomain` runs an existing single R3-R8R2 domain-audit runner
**after** the original and supplementary focused tests pass.

The script checks the local and remote branch, checks the reviewed TeX equation,
backs up both originally modified tracked files and the R3-R9 source, applies
the CLAUSE-only repair, then executes R3-R9's own focused tests and additional
focused source checks. On failure, it restores the backed-up files. It never
runs a full pytest suite. Logs and backups are written to
`%LOCALAPPDATA%\EHPProofTracerRecovery`.

## Verification status

The repair logic passed four isolated safety tests in the package authoring
environment. The full R3-R9 focused suite, actual `pi_14^2` search, web proof,
and all 33 registered n=2 groups must be checked in the user's Windows
repository. This bundle does not claim those checks passed.

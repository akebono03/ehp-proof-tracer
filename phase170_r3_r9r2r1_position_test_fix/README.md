# Phase 170 R3-R9R2R1 — Correct the Citation-Position Test

This package corrects **one incorrectly written supplementary test** in the earlier
R3-R9R2 package. The earlier Windows run demonstrated that the original R3-R9
focused suite passed **46 tests**, including the completed `pi_14^2` search and
Web proof checks, but one supplementary test mistakenly treated the verifier's
`position` return value as a character offset into `Toda_07_2.tex`.

The actual character offset is obtained with `verify_reviewed_toda712(tex)`.
The new test checks that exact source clause separately and checks the original
verifier's return value without assuming it represents a TeX offset.

The existing strict Toda (7.12) text check, all inference rules, the typed
literature bridge, the original R3-R9 runner and its tests remain unchanged.
This bundle copies the preceding narrow `CLAUSE` repair and its four safety tests.
It does **not** claim to change or improve any mathematical proof.

## Prerequisites

* Windows PowerShell, Git, Python and pytest.
* Repository on `develop` commit `fdf60522b6d477209e9d8d67720a63f9863e419c`.
* Existing original `phase170_r3_r9_toda712_cited_rewrite` directory, or
  `phase170_r3_r9_toda712_cited_rewrite.zip` in `Downloads`.
* Internet access for the read-only `git ls-remote origin` verification.
* No unrelated tracked changes and no staged changes.

Two tracked pytest cache files (`.pytest_cache/v/cache/lastfailed` and `nodeids`)
may have been modified by the previous failed run. The runner saves copies of
these files under `%LOCALAPPDATA%\EHPProofTracerRecovery`, restores only
these two cache files from HEAD, and saves after-run cache copies before a final
cache restoration. All other tracked edits cause a refusal before any change.

## Run from the repository root

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase170_r3_r9r2r1_position_test_fix.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -NoProfile `
  -ExecutionPolicy Bypass `
  -File ".\phase170_r3_r9r2r1_position_test_fix\run.ps1"

git status -sb
```

Optional `-AuditOnly` only checks preconditions. Optional `-AuditDomain` runs
an existing R3-R8R2 domain audit after focused tests; use the default run first.
No whole-suite pytest is run.

## Verification

In the authoring environment the isolated repair safety tests pass. The user's
previous original R3-R9 Windows run passed 46 tests and verified `pi_14^2`.
The corrected supplementary test suite and 33-entry domain audit have not yet
been re-run in the user's Windows repository. The runner performs the former;
the latter is optional and should be confirmed separately.

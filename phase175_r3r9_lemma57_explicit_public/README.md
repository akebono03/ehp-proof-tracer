# Phase 175 R3R9 — Direct citation of Toda Lemma 5.7

This package replaces the unnecessary Lemma 5.4 dependency in the **public proof of** `pi_7^3` with the explicit “in particular” conclusion of Toda's Lemma 5.7:

`E(eta_2 o nu-prime) = 0`.

The project's **adopted Japanese Chapter V transcription** states this conclusion directly in the lemma text. The original printed edition has not been independently verified. The general conditional portion of Lemma 5.7 is not used to re-derive this particular conclusion.

The new cited source is a typed `FIXED_STATEMENT` for the text of the explicit clause, **not** a `GeneratorImage` or group result supplied as a `GIVEN`. An ordinary guarded inference extracts the typed generator-image conclusion from this exact citation. The existing verified-prior finite-cyclic zero-image rule, EHP exactness, and finite-cyclic Hopf-lift rules are reused unchanged. No source or mathematical fact is inferred from a target group answer.

Only the already reviewed `search_shared_group_goal` function in `phase165_r52_r9_shared_math.py` is changed: the previous `(n,k)=(3,4)` route import is replaced with this package's route import. All other code, API signatures, and renderer paths are preserved. On verification failure, the installer restores the exact original file bytes.

## Requirements

- Checked-out `develop` branch descended from commit `7171af968ba510291f87b8bb484d8718a3cef204`.
- The previously completed and committed Phase 175 R3R8R1R2 public route.
- The previously successful **normal** R3R8R1R2 report in `%LOCALAPPDATA%\EHPProofTracerAudit`.
- Python and pytest available on PATH.

## Running on Windows

Extract `R3R9.zip` into the repository root.

```powershell
$script = ".\phase175_r3r9_lemma57_explicit_public\run.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
Write-Output "DRYRUN_EXIT_CODE=$LASTEXITCODE"
```

Only if the DryRun exit code is zero, execute:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File $script
Write-Output "R3R9_EXIT_CODE=$LASTEXITCODE"
git status -sb
```

The full test suite is deliberately **not** run during this intermediate Phase step. The bundled audit runs only focused tests and an actual registered Group query and Web verification.

## Success gate

`PASS_R3R9_DIRECT_LEMMA57_PI73_PUBLIC_COMPLETE`

This requires a complete typed proof, trust verification, the `generic-complete-proof` Web result, exactly one inference extracting the cited explicit Lemma 5.7 clause, and **no** dependency on Lemma 5.4 in the accepted proof tree or citations.

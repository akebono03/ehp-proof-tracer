# Phase 173 Final Gate R2R1 — Previous Evidence Location Recovery

This package repairs **only** the existing `phase173_final_gate_r2_recovery/gate.py` and `run.ps1` preflight/runner. It does not change mathematical proof rules, renderers, registered statements, project documentation, or the active `tests/` suite. It does not execute a full suite during patch installation.

## Verified failure and cause

The 2026-11-04 corrective R2 `-DryRun` stopped at `verify_prior_failure()` with `Previous Phase 173 failure evidence is incomplete` **after 14 gate tests passed**. The active suite was not re-executed. R2 originally used the current user's `%LOCALAPPDATA%`, but the earlier failed Phase 173 final gate reported its original evidence under `C:\Users\oomae\AppData\Local\EHPProofTracerRecovery\phase173_final_gate`. The subsequent command was executed as `C:\Users\user\...`. This account-path difference explains why the prior file set could not be found; actual access to the earlier path still needs to be verified on Windows.

Separately, the reviewed GitHub `develop` advanced from `ac9149beaf91eeef382bc816234bd2d895398667` to `25b1ee1f7c848356604061991db06265cfccb296` by committing the three approved Phase 167 reference tests and final gate packages. The corrected snapshot check accepts this specific *type* of reviewed fast-forward, including local unstaged tests identical to the approved R1 patch. It does not fetch or merge files into the user's local checkout, stage changes, reset branches, or erase the original failure.

## Inputs and precise boundaries

Original source files must be byte-for-byte the earlier R2 distribution (`gate.py` SHA-256 `f282ff57...`, `run.ps1` SHA-256 `0892e724...`) or already equal the fully reviewed replacement. The patch program rejects any unknown local alterations and preserves the original bytes under `phase173_final_gate_r2r1_evidence_path_recovery/original_backups/` before replacement.

The repaired `run.ps1` selects one **existing** four-file prior-evidence directory, in this order: explicitly supplied `-PreviousEvidencePath`, complete evidence under current `%LOCALAPPDATA%`, and complete evidence under the previously reported `C:\Users\oomae\AppData\Local\EHPProofTracerRecovery\phase173_final_gate`. A missing/inaccessible directory produces an explicit missing-file report and does not start the active suite. The original data are **read only**, never silently fabricated, copied, overwritten or removed. The existing R2 verifier still checks the previous report's `FAIL`, pytest exit code 1, five named failures, and `5 failed, 3541 passed` summary.

The reviewed code hashes, committed path allowlist, and exact three repaired-test SHA-256 digests remain required. If `origin/develop` advances beyond the reviewed source or changes any non-approved file, the corrected gate still fails closed. Local and remote history must be an actual fast-forward, not a divergence. Source blobs are checked on both sides of a reviewed HEAD mismatch.

## Install and execute

From the Git repository root in PowerShell:

```powershell
$ErrorActionPreference = 'Stop'
Expand-Archive -Path "$HOME\Downloads\EHP_Phase173_FINAL_GATE_R2R1_PRIOR_EVIDENCE_PATH_FIX.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_final_gate_r2r1_evidence_path_recovery\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw 'R2R1 DryRun failed' }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_final_gate_r2r1_evidence_path_recovery\run.ps1"
if ($LASTEXITCODE -ne 0) { throw 'R2R1 install failed' }
```

This performs **focused tests only**. To run the repaired R2 gate, call the original R2 path, optionally specifying an actual previous-evidence directory:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_final_gate_r2_recovery\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw 'Corrected R2 DryRun failed' }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_final_gate_r2_recovery\run.ps1"
if ($LASTEXITCODE -ne 0) { throw 'Corrected R2 final gate failed' }
```

If the original failure files are at a different location, add `-PreviousEvidencePath 'C:\actual\path\to\phase173_final_gate'` to **both** corrected R2 calls. Do not create dummy reports or reuse the new R2 evidence directory as the old failure source.

## Completion conditions

R2R1 patch: `PHASE173_FINAL_R2R1_INSTALL=PASS`, `PHASE173_FINAL_R2R1_FOCUSED_PYTEST=PASS`, `PHASE173_FINAL_R2R1_APPLY=PASS`, and Git index preservation. Corrected R2 dry run: `PHASE173_FINAL_R2_PRIOR_FAILURE_PRESERVED=PASS` and `PHASE173_FINAL_R2_PREFLIGHT=PASS`. The subsequent normal R2 run must report `3546 passed` and exit code zero **before** claiming the final active suite succeeded. Phase 173 remains formally open until the final evidence is documented and reviewed; browser pixel-level MathJax layout is independently unconfirmed.

# Phase 173 — Final Gate R2R2: missing historical evidence handling

This package corrects the recovery path when an earlier failed full-suite log was stored under a Windows profile that is not accessible to the present checkout. It never creates, copies, deletes, or modifies the historical four-file failure evidence.

It changes only the full `gate.py` and `run.ps1` files inside `phase173_final_gate_r2_recovery/`. The patcher verifies both exact current SHA-256 values and saves their original bytes before replacing them. `-DryRun` changes no production file. `git reset`, `git clean`, staging, and committing are never invoked.

The corrected R2 Gate retains strict verification by default. Only an explicit `-AllowMissingPriorEvidence` switch permits proceeding when **all four** original evidence files are absent from the selected evidence directory. A partially available or inconsistent historical record is rejected. The new attempt and report transparently record `prior_failure_evidence_status=UNAVAILABLE_ORIGINAL_FILES`, an empty `prior_failure_sha256` object, and `PHASE173_FINAL_R2_PRIOR_FAILURE_PRESERVED=NOT_VERIFIABLE`. The earlier console log remains available in the ChatGPT discussion, not as an authenticated machine file.

The actual active `tests/` suite is executed only by the corrected R2 Gate's **normal** execution, never by this patcher. The existing source guards, reviewed R1 test SHA-256 checks, 3,546-pass requirement, exclusive attempt marker, and non-overwriting report behavior are unchanged. The corrective report remains in `%LOCALAPPDATA%\EHPProofTracerRecovery\phase173_final_gate_r2\` and the original report directory is not touched.

## Installation

From repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase173_FINAL_GATE_R2R2_MISSING_EVIDENCE_FIX.zip" -DestinationPath . -Force
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase173_final_gate_r2r2_missing_evidence\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase173_final_gate_r2r2_missing_evidence\run.ps1
```

Only after both commands succeed, run the reviewed corrective R2 Gate using the explicit acknowledgment:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase173_final_gate_r2_recovery\run.ps1 -DryRun -AllowMissingPriorEvidence
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase173_final_gate_r2_recovery\run.ps1 -AllowMissingPriorEvidence
```

Do not use `-AllowMissingPriorEvidence` if any of the historical files are available but incomplete. Supply the real directory using `-PreviousEvidencePath` for a complete original record instead.

The phase is not closed until a successful corrective full-suite run is reviewed and the five primary documents receive the final closeout results. Browser pixel-level layout remains independently unverified.

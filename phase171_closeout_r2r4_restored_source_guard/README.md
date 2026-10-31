# Phase 171 Closeout R2R4 — Restored-source guard correction

This package corrects only the content-guard handling in the existing R2R3 installer. The earlier R2R1 failure restored both R2 Python files to their reviewed R2 originals; R2R3 had accepted only the intermediate R2R1 state. R2R4 recognizes either complete, exactly hashed old pair and rejects mixtures or unknown content.

The existing R2R3 implementation then generates all five full updated documents while preserving historical bytes, runs focused tests, and retains external backups. The phase-end full test suite is deliberately **not** run here.

## Usage (from repository root)

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_Closeout_R2R4_Restored_Source_Guard.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_closeout_r2r4_restored_source_guard\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_closeout_r2r4_restored_source_guard\run.ps1"
git status -sb
git diff --check
git diff --stat
```

Requires existing R2, R2R1 and R2R3 packages, Python and pytest. A failure restores the prior R2R3 installer and delegates restoration of document files to R2R3. Backups and reports are written under `%LOCALAPPDATA%\EHPProofTracerRecovery`.

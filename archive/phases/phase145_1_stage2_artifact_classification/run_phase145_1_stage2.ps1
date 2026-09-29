$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 145-1 Stage 2: Phase Artifact Classification"
Write-Host "Classification only - no deletion"
Write-Host "=============================================================="

python ".\phase145_1_stage2_artifact_classification\audit_phase145_1_stage2.py"
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 145-1 Stage 2 audit finished."
Write-Host "Please paste the summary output back into ChatGPT."
Write-Host "=============================================================="

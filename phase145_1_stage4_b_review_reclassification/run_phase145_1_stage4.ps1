$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 145-1 Stage 4: B_REVIEW reason reclassification"
Write-Host "Audit only - NO DELETION"
Write-Host "=============================================================="

$env:PYTHONIOENCODING = "utf-8"
python ".\phase145_1_stage4_b_review_reclassification\audit_phase145_1_stage4.py"
$code = $LASTEXITCODE
Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue

if ($code -ne 0) {
    exit $code
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 145-1 Stage 4 audit finished."
Write-Host "Please upload phase145_1_stage4_summary.txt to ChatGPT."
Write-Host "=============================================================="

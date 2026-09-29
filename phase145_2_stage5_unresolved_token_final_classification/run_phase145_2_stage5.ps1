$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 145-2 Stage 5: Unresolved Token Final Classification"
Write-Host "Audit only - NO MOVE / NO DELETE / NO CODE CHANGE"
Write-Host "=============================================================="

$env:PYTHONIOENCODING = "utf-8"
python ".\phase145_2_stage5_unresolved_token_final_classification\audit_phase145_2_stage5.py"
$code = $LASTEXITCODE
Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue

if ($code -ne 0) {
    exit $code
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 145-2 Stage 5 audit finished."
Write-Host "Upload:"
Write-Host "  output\phase145_2_stage5_unresolved_token_final_classification_summary.txt"
Write-Host "=============================================================="

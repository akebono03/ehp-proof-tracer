$ErrorActionPreference = "Stop"
Write-Host "=============================================================="
Write-Host "Phase 145-2 Stage 2: Relative Path Risk Refinement"
Write-Host "Audit only - NO MOVE / NO DELETE / NO CODE CHANGE"
Write-Host "=============================================================="
$env:PYTHONIOENCODING = "utf-8"
python ".\phase145_2_stage2_relative_path_risk_refinement\audit_phase145_2_stage2.py"
$code = $LASTEXITCODE
Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
if ($code -ne 0) { exit $code }
Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 145-2 Stage 2 audit finished."
Write-Host "Upload output\phase145_2_stage2_relative_path_refinement_summary.txt"
Write-Host "=============================================================="

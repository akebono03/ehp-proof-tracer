$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 145-2 Stage 1: Phase Artifact Archiving Audit"
Write-Host "Audit only - NO MOVE / NO DELETE"
Write-Host "=============================================================="

$env:PYTHONIOENCODING = "utf-8"
python ".\phase145_2_stage1_archiving_audit\audit_phase145_2_stage1.py"
$code = $LASTEXITCODE
Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue

if ($code -ne 0) {
    exit $code
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 145-2 Stage 1 audit finished."
Write-Host "Upload output\phase145_2_stage1_archiving_summary.txt to ChatGPT."
Write-Host "=============================================================="

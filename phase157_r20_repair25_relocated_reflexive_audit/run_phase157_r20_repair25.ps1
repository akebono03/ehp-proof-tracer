$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair25 - relocated reflexive audit"
Write-Host "=============================================================="
Write-Host "Production code changes: none"
Write-Host ""

$env:PYTHONPATH = (Get-Location).Path

python ".\phase157_r20_repair25_relocated_reflexive_audit\audit_phase157_r20_repair25.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "No pytest is run."
Write-Host "No production file is modified."

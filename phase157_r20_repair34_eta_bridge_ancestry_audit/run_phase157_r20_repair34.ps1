$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair34 - eta bridge ancestry audit"
Write-Host "=============================================================="
Write-Host "Production code changes: none"
Write-Host ""

$env:PYTHONPATH = (Get-Location).Path

python ".\phase157_r20_repair34_eta_bridge_ancestry_audit\audit_phase157_r20_repair34.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "No pytest is run."
Write-Host "No production file is modified."

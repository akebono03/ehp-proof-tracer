$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair17 - eta bridge runtime audit"
Write-Host "=============================================================="
Write-Host "Production code changes: none"
Write-Host ""

$env:PYTHONPATH = (Get-Location).Path

python ".\phase157_r20_repair17_eta_bridge_runtime_audit\audit_phase157_r20_repair17.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "No pytest is run."
Write-Host "No production file is modified."

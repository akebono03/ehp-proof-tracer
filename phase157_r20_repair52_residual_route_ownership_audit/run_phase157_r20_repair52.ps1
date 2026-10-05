$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair52 - residual route ownership audit"
Write-Host "=============================================================="
Write-Host "Production code changes: none"
Write-Host "Repository-wide pytest: not run"
Write-Host ""

$env:PYTHONPATH = (Get-Location).Path

python ".\phase157_r20_repair52_residual_route_ownership_audit\audit_phase157_r20_repair52.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "No production file is modified."
Write-Host "No pytest is run."

$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair50 - cross-audit finding classification"
Write-Host "=============================================================="
Write-Host "Production code changes: none"
Write-Host "Repository-wide pytest: not run"
Write-Host ""

$env:PYTHONPATH = (Get-Location).Path

python ".\phase157_r20_repair50_cross_audit_finding_classification\audit_phase157_r20_repair50.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "No production file is modified."
Write-Host "No pytest is run."

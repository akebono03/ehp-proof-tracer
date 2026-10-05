$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair21 - base renderer reflexive audit"
Write-Host "=============================================================="
Write-Host "Production code changes: none"
Write-Host ""

$env:PYTHONPATH = (Get-Location).Path

python ".\phase157_r20_repair21_base_renderer_reflexive_audit\audit_phase157_r20_repair21.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "No pytest is run."
Write-Host "No production file is modified."

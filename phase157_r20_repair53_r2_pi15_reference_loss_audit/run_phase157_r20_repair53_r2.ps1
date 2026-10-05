$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair53-r2 - pi15 Proposition 4.4 reference loss audit"
Write-Host "=============================================================="
Write-Host "Production code changes: none"
Write-Host "Repository-wide pytest: not run"
Write-Host ""

$env:PYTHONPATH = (Get-Location).Path

python ".\phase157_r20_repair53_r2_pi15_reference_loss_audit\audit_phase157_r20_repair53_r2.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "No production file is modified."
Write-Host "No pytest is run."

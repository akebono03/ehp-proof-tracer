$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair53-r3b - pi15 Reference number audit"
Write-Host "=============================================================="
Write-Host "Production code changes: none"
Write-Host "Repository-wide pytest: not run"
Write-Host ""

$env:PYTHONPATH = (Get-Location).Path

python ".\phase157_r20_repair53_r3b_pi15_reference_number_audit\audit_phase157_r20_repair53_r3b.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "No production file is modified."
Write-Host "No pytest is run."

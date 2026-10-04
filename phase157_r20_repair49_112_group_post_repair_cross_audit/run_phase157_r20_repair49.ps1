$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair49 - 112-group post-repair cross-audit"
Write-Host "=============================================================="
Write-Host "Production code changes: none"
Write-Host "Repository-wide pytest: not run"
Write-Host ""

$env:PYTHONPATH = (Get-Location).Path

python ".\phase157_r20_repair49_112_group_post_repair_cross_audit\audit_phase157_r20_repair49.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "Summary:"
Get-Content `
  ".\phase157_r20_repair49_112_group_post_repair_cross_audit\audit_output\summary.txt"

Write-Host ""
Write-Host "No production file is modified."
Write-Host "No pytest is run."

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python -m pytest -q "$PSScriptRoot\test_audit.py"
if ($LASTEXITCODE -ne 0) { throw 'R6-14 package tests failed; audit not run' }
python "$PSScriptRoot\audit.py"
if ($LASTEXITCODE -ne 0) { Write-Host 'R6-14 audit found blockers. Inspect phase165_r6_audit_results\r6_14_final_audit\report.json'; exit 2 }
Write-Host 'R6-14 READY. Full pytest NOT run.'

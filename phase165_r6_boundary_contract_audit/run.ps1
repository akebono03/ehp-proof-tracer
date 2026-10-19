$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
Write-Host 'Phase 165 R6 boundary contract audit (4 targeted tests only)'
python -m pytest -q '.\phase165_r6_boundary_contract_audit\test_boundary_contract.py'
if ($LASTEXITCODE -ne 0) { throw "Boundary audit failed; exit=$LASTEXITCODE" }
Write-Host 'Boundary audit PASS; production files unchanged; full pytest NOT run.'

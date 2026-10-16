$ErrorActionPreference = 'Stop'
$package = $PSScriptRoot
$root = (Get-Location).Path
if (-not (Test-Path (Join-Path $root 'phase165_r8_rule_provider.py'))) {
    throw 'Run from the ehp_proof repository root.'
}
$python = 'python'
& $python -m pytest -q (Join-Path $package 'test_inventory.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-A targeted tests failed' }
& $python (Join-Path $package 'inventory.py') --root $root --out (Join-Path $package 'reports')
if ($LASTEXITCODE -ne 0) { throw 'R4-A audit failed' }
Write-Host 'Output: phase165_r6_2_r4_a_inventory\reports\rule_inventory.json and .md'
Write-Host 'Full pytest NOT run. Production files unchanged.'

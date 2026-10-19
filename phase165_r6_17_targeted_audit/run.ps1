$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Join-Path $root 'phase165_r6_17_targeted_audit'
if (-not (Test-Path (Join-Path $package 'audit.py'))) { throw 'Please run from repository root.' }
python -m pytest -q (Join-Path $package 'test_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R6-17 package tests failed; audit not run.' }
python (Join-Path $package 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R6-17 audit found missing or invalid source; inspect report.' }
Write-Host 'R6-17 read-only audit completed. Full pytest NOT run.'

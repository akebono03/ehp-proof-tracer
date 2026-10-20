$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = $PSScriptRoot

python (Join-Path $package 'apply.py')
if ($LASTEXITCODE -ne 0) { throw 'R3-Q patch failed' }

python -m pytest -q `
  (Join-Path $package 'tests\test_phase166_r3q_web_publication_order.py') `
  'phase166_r3d_pi32_regression\tests\test_phase166_r3d_pi32_regression.py'
if ($LASTEXITCODE -ne 0) { throw 'R3-Q targeted tests failed' }

Write-Host 'R3-Q targeted tests PASS; full pytest NOT run.'

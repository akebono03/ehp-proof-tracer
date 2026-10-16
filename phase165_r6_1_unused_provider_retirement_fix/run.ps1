$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
python (Join-Path $PSScriptRoot 'apply.py')
if ($LASTEXITCODE -ne 0) { throw 'Patch failed' }
python -m pytest -q '.\phase165_r52_r7_registered_common_proof\test_phase165_r52_r7_registered_common_proof.py'
if ($LASTEXITCODE -ne 0) { throw 'Focused tests failed' }
Write-Host 'Legacy pi3_2 provider route retired (runner fix); full pytest NOT run.'

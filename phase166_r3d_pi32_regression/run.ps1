$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
python -m pytest -q '.\phase166_r3d_pi32_regression\tests\test_phase166_r3d_pi32_regression.py'
if ($LASTEXITCODE -ne 0) { throw 'R3-D pi3^2 regression failed' }
Write-Output 'Phase 166 R3-D targeted PASS; production code unchanged; full pytest NOT run.'

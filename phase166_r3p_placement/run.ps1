$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project
python (Join-Path $PSScriptRoot 'apply.py')
if ($LASTEXITCODE -ne 0) { throw 'R3-P patch failed' }
python -m pytest -q (Join-Path $PSScriptRoot 'tests/test_phase166_r3p_positions.py')
if ($LASTEXITCODE -ne 0) { throw 'R3-P focused tests failed' }
Write-Output 'R3-P focused tests PASS; full pytest NOT run.'

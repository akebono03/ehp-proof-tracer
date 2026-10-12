$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = "$PSScriptRoot;$root"
if (!(Test-Path '.\phase163_r4_r74_output\remaining_boundary_proposals.json')) { throw 'Missing R74 output; run R74 first' }
python -m pytest -q "$PSScriptRoot\tests\test_phase163_r4_r75_boundary_ownership.py"
if ($LASTEXITCODE -ne 0) { throw 'R75 focused pytest failed' }
python "$PSScriptRoot\phase163_r4_r75_boundary_ownership.py"
if ($LASTEXITCODE -ne 0) { throw 'R75 ownership review failed' }
Write-Host 'R75 complete. No production changes. Full pytest not run.'

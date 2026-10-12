$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = "$PSScriptRoot;$root"
python -m pytest -q "$PSScriptRoot\tests\test_phase163_r4_r74_remaining_context_review.py"
if ($LASTEXITCODE -ne 0) { throw 'R74 focused pytest failed' }
python "$PSScriptRoot\phase163_r4_r74_remaining_context_review.py"
if ($LASTEXITCODE -ne 0) { throw 'R74 review failed' }
Write-Host 'R74 complete. No production changes. Full pytest not run.'

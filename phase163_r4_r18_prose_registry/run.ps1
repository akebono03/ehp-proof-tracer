$ErrorActionPreference = 'Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))
python -B -m pytest -q .\phase163_r4_r18_prose_registry\tests\test_integrate.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m phase163_r4_r18_prose_registry.integrate --source .\phase163_r4_r18_prose_registry\Toda_01.tex --output .\phase163_r4_r18_output
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R4-R18 completed; no production code changed and full suite not run.'

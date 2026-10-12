$ErrorActionPreference = 'Stop'
$project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $project
$env:PYTHONPATH = $PSScriptRoot
python -m pytest -q (Join-Path $PSScriptRoot 'test_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R8-R4 audit tests failed' }
python (Join-Path $PSScriptRoot 'audit.py') --root $project --output (Join-Path $project 'phase164_r8_r4_output')
if ($LASTEXITCODE -ne 0) { throw 'R8-R4 inventory failed; inspect parse errors' }
Get-Content (Join-Path $project 'phase164_r8_r4_output\report.md') -Encoding UTF8 | Select-Object -First 30
Write-Host 'R8-R4 planning audit complete; no production modifications; full pytest NOT run.'

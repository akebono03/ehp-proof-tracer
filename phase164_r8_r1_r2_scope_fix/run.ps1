$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
if (-not (Test-Path (Join-Path $project 'proof.py'))) { throw 'Run from project root containing proof.py' }
$script = Join-Path $PSScriptRoot 'audit.py'
$env:PYTHONDONTWRITEBYTECODE = '1'
python -B -m pytest -q -p no:cacheprovider (Join-Path $PSScriptRoot 'test_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R8-R1-R2 audit tests failed' }
python -B $script
if ($LASTEXITCODE -ne 0) { throw 'R8-R1-R2 audit failed' }
Write-Host 'R8-R1-R2 read-only inventory complete; full pytest NOT run.'

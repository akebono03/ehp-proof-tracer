$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path (Join-Path $root 'phase165_r8_rule_provider.py'))) { throw 'Run from the repository root.' }
$env:PYTHONDONTWRITEBYTECODE = '1'
python -B -m pytest -q -p no:cacheprovider (Join-Path $PSScriptRoot 'test_r3_probe.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-A-R3 targeted pytest failed.' }
python -B (Join-Path $PSScriptRoot 'r3_probe.py') --root $root --out (Join-Path $PSScriptRoot 'reports')
if ($LASTEXITCODE -ne 0) { throw 'R4-A-R3 audit incomplete.' }
Write-Output 'Full pytest NOT run. Production files unchanged.'

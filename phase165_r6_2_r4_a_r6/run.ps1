$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path (Join-Path $root 'phase165_r8_rule_provider.py'))) { throw 'Run from repository root.' }
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONPATH = "$root;$PSScriptRoot"
python -B -m pytest -q -p no:cacheprovider (Join-Path $PSScriptRoot 'test_r6_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-A-R6 targeted tests failed.' }
python -B (Join-Path $PSScriptRoot 'r6_audit.py') --root $root --out (Join-Path $PSScriptRoot 'reports')
if ($LASTEXITCODE -ne 0) { throw 'R4-A-R6 audit failed.' }
Write-Output 'Full pytest NOT run. Production files unchanged.'

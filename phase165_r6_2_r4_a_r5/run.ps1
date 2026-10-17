$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path (Join-Path $root 'phase165_r8_rule_provider.py'))) { throw 'Run from repository root.' }
if (-not (Test-Path (Join-Path $root 'phase165_r6_2_r4_a_r4\r4_probe.py'))) { throw 'R4-A-R4 must be installed first.' }
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONPATH = $PSScriptRoot
python -B -m pytest -q -p no:cacheprovider (Join-Path $PSScriptRoot 'test_r5_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R4-A-R5 targeted tests failed.' }
python -B (Join-Path $PSScriptRoot 'r5_audit.py') --root $root --out (Join-Path $PSScriptRoot 'reports')
if ($LASTEXITCODE -ne 0) { throw 'R4-A-R5 audit incomplete. Check reports.' }
Write-Output 'Full pytest NOT run. Production files unchanged.'

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
python (Join-Path $PSScriptRoot 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R23 installation failed' }
python -m pytest -q (Join-Path $PSScriptRoot 'test_phase165_r52_r23_existing_rule_adapter.py') test_phase165_r52_r9_shared_math.py
if ($LASTEXITCODE -ne 0) { throw 'R23 targeted pytest failed' }
Write-Host 'R23 targeted tests completed; full pytest NOT run.'

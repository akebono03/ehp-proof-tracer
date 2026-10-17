$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo
python ".\phase165_remove_pi43_adapter_r2\audit.py"
if ($LASTEXITCODE -ne 0) { throw "Adapter audit failed" }
$env:PYTHONPATH = "$PSScriptRoot;$repo"
python -m pytest -q ".\phase165_remove_pi43_adapter_r2\test_audit.py"
if ($LASTEXITCODE -ne 0) { throw "Targeted pytest failed" }
Write-Host 'Adapter removal independently confirmed; full pytest NOT run.'

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo
$env:PYTHONPATH = "$PSScriptRoot;$repo"
python ".\phase165_pi43_common_trace_r1\audit.py"
if ($LASTEXITCODE -ne 0) { throw 'Common pi43 trace failed' }
python -m pytest -q ".\phase165_pi43_common_trace_r1\test_audit.py"
if ($LASTEXITCODE -ne 0) { throw 'Focused tests failed' }
Write-Host 'Common pi43 trace completed; full pytest NOT run.'

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
python ".\phase165_r50_delta_reason_repair\apply.py"
if ($LASTEXITCODE -ne 0) { throw 'R50 Delta-reason install failed' }
python -m pytest -q ".\phase165_r50_reference_bridge\test_phase165_r50.py" ".\tests\test_phase165_r49_display_fix.py" ".\tests\test_phase165_r49_typed_reasons.py"
if ($LASTEXITCODE -ne 0) { throw 'R49/R50 targeted tests failed' }
Write-Host 'R49/R50 targeted tests passed; full pytest NOT run.'

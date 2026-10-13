$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python "$PSScriptRoot\apply.py"
if ($LASTEXITCODE -ne 0) { throw 'R50 repair installation failed' }
python -m pytest -q "phase165_r50_reference_bridge\test_phase165_r50.py" "tests\test_phase165_r49_display_fix.py"
if ($LASTEXITCODE -ne 0) { throw 'R50/R49 targeted tests failed' }
Write-Host 'R50/R49 targeted tests passed; full pytest NOT run.'

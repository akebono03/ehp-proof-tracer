$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python "$PSScriptRoot\apply.py"
if ($LASTEXITCODE -ne 0) { throw "R49 repair install failed" }
python -m pytest -q tests/test_phase165_r49_typed_reasons.py tests/test_phase165_r49_display_fix.py
if ($LASTEXITCODE -ne 0) { throw "R49 targeted tests failed" }
Write-Host "R49 targeted tests passed; full pytest NOT run."

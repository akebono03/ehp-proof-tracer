$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

python "$PSScriptRoot\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python -m pytest -q `
  "$PSScriptRoot\test_phase165_r13_r1_contract.py" `
  "tests/test_phase164_r5_r2_unified_web_display.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Phase 165 R13-R1 targeted verification passed; full pytest NOT run."

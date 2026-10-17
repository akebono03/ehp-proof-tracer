$ErrorActionPreference = "Stop"
$root = (Get-Location).Path
python ".\phase165_r12_r2_quotient_rules\install.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q tests/test_phase165_r12_r2_quotient_rules.py tests/test_phase165_r8_rule_provider.py tests/test_phase165_r11_wiring.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R12-R2 targeted tests completed; full pytest NOT run."

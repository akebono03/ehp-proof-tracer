$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python -m phase165_r12_r3_generic_connection.audit
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q `
  phase165_r12_r3_generic_connection/tests/test_phase165_r12_r3_generic_connection.py `
  tests/test_phase165_r8_rule_provider.py `
  tests/test_phase165_r11_wiring.py
exit $LASTEXITCODE

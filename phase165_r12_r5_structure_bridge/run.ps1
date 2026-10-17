$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
& python (Join-Path $PSScriptRoot 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R12-R5 installation failed.' }
& python -m pytest -q '.\tests\test_phase165_r12_r5_structure_bridge.py' '.\tests\test_phase165_r8_rule_provider.py' '.\tests\test_phase165_r11_wiring.py'
if ($LASTEXITCODE -ne 0) { throw 'R12-R5 targeted pytest failed.' }
& python -m phase165_r12_r5_structure_bridge_audit
if ($LASTEXITCODE -ne 0) { throw 'R12-R5 bridge audit failed.' }
Write-Host 'R12-R5 focused tests finished; full pytest NOT run.'

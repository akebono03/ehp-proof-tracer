$ErrorActionPreference = 'Stop'
$Root = (Get-Location).Path
$Package = $PSScriptRoot
python -m pytest -q (Join-Path $Package 'test_install.py')
if ($LASTEXITCODE -ne 0) { throw 'Installer tests failed' }
python (Join-Path $Package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'Rule installation failed' }
python -m pytest -q (Join-Path $Package 'test_integration.py') 'tests/test_map_property_rules.py' 'tests/test_phase165_r8_rule_provider.py'
if ($LASTEXITCODE -ne 0) { throw 'Targeted integration tests failed' }
Write-Host 'R4-4 stage2 installed; targeted tests PASS; full pytest NOT run.'

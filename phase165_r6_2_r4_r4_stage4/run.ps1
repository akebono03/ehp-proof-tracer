$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = (Resolve-Path (Join-Path $here '..')).Path
Set-Location $root
$env:PYTHONPATH = $root
python -m pytest -q (Join-Path $here 'test_install.py')
if ($LASTEXITCODE -ne 0) { throw 'Installer tests failed' }
python (Join-Path $here 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'Stage4 installation failed' }
python -m pytest -q (Join-Path $here 'test_integration.py') 'tests/test_map_property_rules.py' 'tests/test_phase165_r8_rule_provider.py'
if ($LASTEXITCODE -ne 0) { throw 'Stage4 targeted regression failed' }
Write-Output 'R4-4 stage4 installed; targeted tests PASS; full pytest NOT run.'

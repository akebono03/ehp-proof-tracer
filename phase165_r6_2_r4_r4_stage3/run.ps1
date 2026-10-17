$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = (Resolve-Path (Join-Path $here '..')).Path
Set-Location $root
python -m pytest -q (Join-Path $here 'test_install.py')
if ($LASTEXITCODE -ne 0) { throw 'Installer tests failed' }
python (Join-Path $here 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'Installation failed' }
python -m pytest -q (Join-Path $here 'test_integration.py') 'tests/test_map_property_rules.py' 'tests/test_ehp_rules.py' 'tests/test_phase165_r8_rule_provider.py'
if ($LASTEXITCODE -ne 0) { throw 'Targeted integration tests failed' }
Write-Output 'R4-4 stage3 complete; full pytest NOT run.'

$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$package\install.py"
if ($LASTEXITCODE -ne 0) { throw 'R19 installation failed' }
$required = @('test_phase165_r52_r19_prop51_binding.py', 'test_phase165_r52_r18_proof_order.py', 'test_phase165_r52_r9_shared_math.py')
foreach ($name in $required) { if (-not (Test-Path ".\$name")) { throw "Required test missing: $name" } }
python -m pytest -q @required
if ($LASTEXITCODE -ne 0) { throw 'R19 targeted tests failed' }
Write-Host 'R19 targeted tests passed; full pytest NOT run.'

$ErrorActionPreference = 'Stop'
$base = Split-Path -Parent $PSScriptRoot
Set-Location $base
python ".\phase165_r6_2_r4_r12_root_gate_fix\install.py"
if ($LASTEXITCODE -ne 0) { throw 'R4-R12 installation failed' }
python -m pytest -q ".\phase165_r6_2_r4_r12_root_gate_fix\test_r4_r12.py" ".\tests\test_phase165_r3_recursive_search.py"
if ($LASTEXITCODE -ne 0) { throw 'R4-R12 focused regression failed' }
Write-Host 'R4-R12 installed, focused tests passed, full pytest NOT run.'

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python '.\phase166_r3f_order_fix\install.py'
if ($LASTEXITCODE -ne 0) { throw 'Installation failed' }
python -m pytest -q '.\phase166_r3f_order_fix\tests\test_phase166_r3f_order_fix.py' '.\phase165_r12_r7_proof_order_revision\tests\test_phase165_r12_r7_proof_order_revision.py'
if ($LASTEXITCODE -ne 0) { throw 'Targeted tests failed' }
Write-Host 'R3-F targeted tests PASS; full pytest NOT run.'

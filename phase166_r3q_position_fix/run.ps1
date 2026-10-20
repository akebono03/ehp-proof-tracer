$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
$env:PYTHONPATH = $root
python -m phase166_r3q_position_fix.install
if ($LASTEXITCODE -ne 0) { throw 'R3-Q position patch failed' }
python -m pytest -q phase166_r3q_position_fix/tests/test_phase166_r3q_position_fix.py phase166_r3d_pi32_regression/tests/test_phase166_r3d_pi32_regression.py phase165_r52_r12_component_bridge/test_phase165_r52_r12_component_bridge.py
if ($LASTEXITCODE -ne 0) {
  python -m phase166_r3q_position_fix.restore
  throw 'R3-Q targeted tests failed; original source restored'
}
Write-Host 'R3-Q position tests PASS. Full pytest NOT run.'

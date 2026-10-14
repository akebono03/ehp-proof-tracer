$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Join-Path $PSScriptRoot 'install.py'
python $package
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q test_phase165_r52_r13_r3_compat_fix.py test_phase165_r52_r13_r2_generic_reference_fix.py test_phase165_r52_r13_r1_collision_fix.py test_phase165_r52_r13_reference_registration.py test_phase165_r52_r12_component_bridge.py test_phase165_r52_r9_shared_math.py
exit $LASTEXITCODE

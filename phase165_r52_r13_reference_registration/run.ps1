$ErrorActionPreference = 'Stop'
python ".\phase165_r52_r13_reference_registration\install.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q test_phase165_r52_r13_reference_registration.py test_phase165_r52_r12_component_bridge.py test_phase165_r52_r9_shared_math.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R52-R13 targeted tests passed; full pytest NOT run.'

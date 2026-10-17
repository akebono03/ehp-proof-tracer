$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python '.\phase165_prop51_literature_r6_fix\install.py'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q '.\phase165_prop51_literature_r6_fix\test_prop51_literature.py' '.\test_phase165_r52_r13_reference_registration.py'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R6 FIX targeted pytest passed; full pytest NOT run.'

$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python (Join-Path $PSScriptRoot 'install.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q `
  (Join-Path $PSScriptRoot 'test_installer.py') `
  (Join-Path $PSScriptRoot 'test_r5_typed_references.py') `
  'test_phase165_r52_r9_shared_math.py::test_r9_pi32_regenerated_by_shared_mathematical_expansion'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R27-R5-R1 targeted tests passed; full pytest NOT run.'

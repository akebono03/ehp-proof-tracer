$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python (Join-Path $PSScriptRoot 'install.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q `
  (Join-Path $PSScriptRoot 'test_install.py') `
  'test_phase165_r52_r9_shared_math.py'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R27-R2 targeted tests passed; full pytest NOT run.'

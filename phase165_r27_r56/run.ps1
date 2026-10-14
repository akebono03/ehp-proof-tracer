$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
  python '.\phase165_r27_r56\apply.py'
  if ($LASTEXITCODE -ne 0) { throw 'R56 installation failed' }
  python -m pytest -q '.\phase165_r27_r56\test_installer.py'
  if ($LASTEXITCODE -ne 0) { throw 'R56 targeted tests failed' }
  Write-Host 'R27-R56 targeted tests passed; full pytest NOT run.'
} finally { Pop-Location }

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
  python ".\phase165_r27_r51_r1\apply.py"
  if ($LASTEXITCODE -ne 0) { throw 'R51-R1 installation failed' }
  python -m pytest -q ".\phase165_r27_r51_r1\test_installer.py"
  if ($LASTEXITCODE -ne 0) { throw 'R51-R1 targeted pytest failed' }
  Write-Host 'R27-R51-R1 targeted tests passed; full pytest NOT run.'
} finally { Pop-Location }

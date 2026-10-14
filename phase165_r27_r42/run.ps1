$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
  python "$PSScriptRoot\apply.py"
  if ($LASTEXITCODE -ne 0) { throw 'R27-R42 install failed' }
  python -m pytest -q "$PSScriptRoot\test_installer.py"
  if ($LASTEXITCODE -ne 0) { throw 'R27-R42 targeted pytest failed' }
  Write-Host 'R27-R42 targeted tests passed; full pytest NOT run.'
} finally { Pop-Location }

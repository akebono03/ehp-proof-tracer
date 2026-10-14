$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
  python "$PSScriptRoot\apply.py"
  if ($LASTEXITCODE -ne 0) { throw "R27-R44 installation failed" }
  python -m pytest -q "$PSScriptRoot\test_installer.py"
  if ($LASTEXITCODE -ne 0) { throw "R27-R44 targeted tests failed" }
  Write-Output 'R27-R44 targeted tests passed; full pytest NOT run.'
} finally { Pop-Location }

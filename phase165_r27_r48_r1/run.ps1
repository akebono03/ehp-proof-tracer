$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
  python "$PSScriptRoot\apply.py"
  if ($LASTEXITCODE -ne 0) { throw "R48-R1 installation failed" }
  python -m pytest -q "$PSScriptRoot\test_installer.py"
  if ($LASTEXITCODE -ne 0) { throw "R48-R1 targeted tests failed" }
  Write-Host "R27-R48-R1 targeted tests passed; full pytest NOT run."
} finally { Pop-Location }

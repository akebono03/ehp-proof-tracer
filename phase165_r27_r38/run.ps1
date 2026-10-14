$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $root
try {
  python "$PSScriptRoot\apply.py"
  if ($LASTEXITCODE -ne 0) { throw "R27-R38 installation failed" }
  python -m pytest -q "$PSScriptRoot\test_installer.py"
  if ($LASTEXITCODE -ne 0) { throw "R27-R38 targeted tests failed" }
  Write-Host "R27-R38 targeted tests passed; full pytest NOT run."
} finally { Pop-Location }

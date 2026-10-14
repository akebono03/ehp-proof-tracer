$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
  python "$PSScriptRoot\apply.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  python -m pytest -q "$PSScriptRoot\test_installer.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  Write-Host 'R27-R40 targeted checks passed; full pytest NOT run.'
} finally {
  Pop-Location
}

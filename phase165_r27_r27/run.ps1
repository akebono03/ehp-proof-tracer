$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
  python (Join-Path $PSScriptRoot 'apply.py')
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  python -m pytest -q (Join-Path $PSScriptRoot 'test_patch.py')
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  Write-Host 'R27-R27 targeted tests passed; full pytest NOT run.'
} finally {
  Pop-Location
}

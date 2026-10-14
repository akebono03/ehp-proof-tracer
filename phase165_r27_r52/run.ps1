$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
  python (Join-Path $PSScriptRoot 'apply.py')
  if ($LASTEXITCODE -ne 0) { throw 'R52 installation failed' }
  python -m pytest -q (Join-Path $PSScriptRoot 'test_installer.py') (Join-Path $PSScriptRoot 'test_typed_facade.py')
  if ($LASTEXITCODE -ne 0) { throw 'R52 targeted pytest failed' }
  Write-Host 'R27-R52 targeted tests passed; full pytest NOT run.'
}
finally { Pop-Location }

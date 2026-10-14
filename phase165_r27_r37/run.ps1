$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
  python (Join-Path $PSScriptRoot 'apply.py')
  if ($LASTEXITCODE -ne 0) { throw "R27-R37 installer failed" }
  python -m pytest -q (Join-Path $PSScriptRoot 'test_installer.py')
  if ($LASTEXITCODE -ne 0) { throw "R27-R37 targeted pytest failed" }
  Write-Host 'R27-R37 targeted checks passed; full pytest NOT run.'
} finally { Pop-Location }

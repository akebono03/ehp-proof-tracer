$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $projectRoot
try {
  python (Join-Path $PSScriptRoot 'apply.py')
  if ($LASTEXITCODE -ne 0) { throw 'Patch failed' }
  python -m pytest -q (Join-Path $PSScriptRoot 'tests/test_generator_linear_combination.py')
  if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
  Write-Host 'Targeted tests PASS; full pytest NOT run.'
}
finally {
  Pop-Location
}

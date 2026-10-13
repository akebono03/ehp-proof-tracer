$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
if (Get-Command python -ErrorAction SilentlyContinue) {
  & python (Join-Path $PSScriptRoot 'apply.py')
  if ($LASTEXITCODE -ne 0) { throw 'R50 installation failed' }
  & python -m pytest -q (Join-Path $PSScriptRoot 'test_phase165_r50.py')
  if ($LASTEXITCODE -ne 0) { throw 'R50 targeted tests failed' }
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
  & py -3 (Join-Path $PSScriptRoot 'apply.py')
  if ($LASTEXITCODE -ne 0) { throw 'R50 installation failed' }
  & py -3 -m pytest -q (Join-Path $PSScriptRoot 'test_phase165_r50.py')
  if ($LASTEXITCODE -ne 0) { throw 'R50 targeted tests failed' }
} else { throw 'Python 3 not found' }
Write-Host 'R50 targeted tests passed; full pytest NOT run.'

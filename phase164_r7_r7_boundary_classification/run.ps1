$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Join-Path $PSScriptRoot 'audit.py'
Push-Location $PSScriptRoot
try {
  python -m pytest -q test_audit.py
  if ($LASTEXITCODE -ne 0) { throw 'R7-R7 audit tests failed' }
} finally { Pop-Location }
python $package --root $root --output (Join-Path $root 'phase164_r7_r7_output')
if ($LASTEXITCODE -ne 0) { throw 'R7-R7 audit failed' }
Write-Host 'Phase 164 R7-R7 classified; production unchanged; full pytest NOT run.'

$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
Push-Location $root
try {
  python -m pytest -q (Join-Path $package 'tests\test_phase168_r3_40f_residual_route_audit.py')
  if ($LASTEXITCODE -ne 0) { throw 'R3-40F limited tests failed' }
  python -m phase168_r3_40f_residual_route_audit.audit
  if ($LASTEXITCODE -ne 0) { throw 'R3-40F read-only audit failed' }
  Write-Host 'R3-40F audit complete. No implementation files modified. Full pytest NOT run.'
}
finally { Pop-Location }

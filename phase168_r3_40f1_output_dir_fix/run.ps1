
$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
$target = Join-Path $root 'phase168_r3_40f_residual_route_audit'
$stamp = Get-Date -Format 'yyyyMMddTHHmmssfff'
$backup = Join-Path $package ("backup\" + $stamp)
New-Item -ItemType Directory -Force -Path (Join-Path $backup 'tests') | Out-Null
if (-not (Test-Path (Join-Path $target 'audit.py'))) { throw 'R3-40F audit.py not found' }
if (-not (Test-Path (Join-Path $target 'tests\test_phase168_r3_40f_residual_route_audit.py'))) { throw 'R3-40F test not found' }
Copy-Item (Join-Path $target 'audit.py') (Join-Path $backup 'audit.py')
Copy-Item (Join-Path $target 'tests\test_phase168_r3_40f_residual_route_audit.py') (Join-Path $backup 'tests\test_phase168_r3_40f_residual_route_audit.py')
Push-Location $root
try {
  python (Join-Path $package 'apply.py')
  if ($LASTEXITCODE -ne 0) { throw 'R3-40F1 patch validation failed' }
  python -m pytest -q (Join-Path $target 'tests\test_phase168_r3_40f_residual_route_audit.py')
  if ($LASTEXITCODE -ne 0) { throw 'R3-40F focused tests failed' }
  python -m phase168_r3_40f_residual_route_audit.audit
  if ($LASTEXITCODE -ne 0) { throw 'R3-40F read-only audit failed' }
  Write-Host 'R3-40F1 completed. Audit-only fix; project implementation unchanged. Full pytest NOT run.'
}
catch {
  Copy-Item (Join-Path $backup 'audit.py') (Join-Path $target 'audit.py') -Force
  Copy-Item (Join-Path $backup 'tests\test_phase168_r3_40f_residual_route_audit.py') (Join-Path $target 'tests\test_phase168_r3_40f_residual_route_audit.py') -Force
  Write-Host ('ROLLBACK: R3-40F audit and test restored from ' + $backup)
  throw
}
finally { Pop-Location }

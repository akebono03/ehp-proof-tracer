$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
$stamp = (Get-Date).ToString('yyyyMMddTHHmmss')
$backup = Join-Path $package ("backup\" + $stamp)
$names = @(
  'phase168_r3_29_order_projection.py',
  'phase168_r3_27_typed_statement_projection.py',
  'phase168_r3_5_model_renderer.py'
)
New-Item -ItemType Directory -Path $backup -Force | Out-Null
foreach ($name in $names) {
  $source = Join-Path $project $name
  if (!(Test-Path $source)) { throw "Missing project file: $source" }
  Copy-Item $source (Join-Path $backup $name) -Force
}
Push-Location $project
try {
  python (Join-Path $package 'apply.py')
  if ($LASTEXITCODE -ne 0) { throw 'Patch application failed' }
  python -m pytest -q `
    (Join-Path $package 'tests\test_phase168_r3_40c_dependency_preserving_order.py') `
    (Join-Path $package 'tests\test_phase168_r3_40d_runner_module_fix.py') `
    '.\phase168_r3_29_order_projection\tests\test_phase168_r3_29_order_projection.py' `
    '.\phase168_r3_27_typed_projection\tests\test_phase168_r3_27_typed_projection.py' `
    '.\phase168_r3_39f_frozen_comparison\tests\test_audit.py'
  if ($LASTEXITCODE -ne 0) { throw 'Limited pytest failed' }
  python -m phase168_r3_40d_runner_module_fix.check_and_capture
  if ($LASTEXITCODE -ne 0) { throw 'Dependency audit failed' }
  python -m phase168_r3_39f_frozen_comparison.audit
  if ($LASTEXITCODE -ne 0) { throw 'Frozen narrative audit failed' }
  Write-Host 'R3-40D runner validation complete; R3-40C projection retained. Full pytest NOT run.'
}
catch {
  foreach ($name in $names) {
    Copy-Item (Join-Path $backup $name) (Join-Path $project $name) -Force
  }
  Write-Host "ROLLBACK: original implementation files restored from $backup"
  throw
}
finally {
  Pop-Location
}

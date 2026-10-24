$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
$target = Join-Path $project 'phase168_r3_5_model_renderer.py'
$stamp = (Get-Date).ToString('yyyyMMddTHHmmss')
$backup = Join-Path $package ("backup\" + $stamp)
if (!(Test-Path $target)) { throw "Missing project Renderer: $target" }
New-Item -ItemType Directory -Path $backup -Force | Out-Null
Copy-Item $target (Join-Path $backup 'phase168_r3_5_model_renderer.py') -Force
Push-Location $project
try {
  python -m phase168_r3_40e_remove_deferred_render.capture_narratives before
  if ($LASTEXITCODE -ne 0) { throw 'Pre-change narrative capture failed' }
  python -m phase168_r3_40e_remove_deferred_render.apply
  if ($LASTEXITCODE -ne 0) { throw 'R3-40E patch failed' }
  python -m pytest -q `
    (Join-Path $package 'tests\test_phase168_r3_40e_remove_deferred_render.py') `
    '.\phase168_r3_40d_runner_module_fix\tests\test_phase168_r3_40c_dependency_preserving_order.py' `
    '.\phase168_r3_40d_runner_module_fix\tests\test_phase168_r3_40d_runner_module_fix.py' `
    '.\phase168_r3_29_order_projection\tests\test_phase168_r3_29_order_projection.py' `
    '.\phase168_r3_27_typed_projection\tests\test_phase168_r3_27_typed_projection.py' `
    '.\phase168_r3_39f_frozen_comparison\tests\test_audit.py'
  if ($LASTEXITCODE -ne 0) { throw 'Limited pytest failed' }
  python -m phase168_r3_40e_remove_deferred_render.capture_narratives after
  if ($LASTEXITCODE -ne 0) { throw 'Narrative byte-comparison failed' }
  python -m phase168_r3_40d_runner_module_fix.check_and_capture
  if ($LASTEXITCODE -ne 0) { throw 'Four-group dependency audit failed' }
  python -m phase168_r3_39f_frozen_comparison.audit
  if ($LASTEXITCODE -ne 0) { throw 'Frozen narrative comparison failed' }
  Write-Host 'R3-40E complete: legacy deferred rendering removed. Full pytest NOT run.'
}
catch {
  Copy-Item (Join-Path $backup 'phase168_r3_5_model_renderer.py') $target -Force
  Write-Host "ROLLBACK: common Renderer restored from $backup"
  throw
}
finally {
  Pop-Location
}

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$package = 'phase169_r4g_hopf_reference'
$targetA = Join-Path $root 'phase165_r52_r27_r5_literature.py'
$targetB = Join-Path $root 'phase168_r3_37c_reference_projection.py'
$beforeA = Join-Path $PSScriptRoot 'output\phase165_r52_r27_r5_literature.py.before'
$beforeB = Join-Path $PSScriptRoot 'output\phase168_r3_37c_reference_projection.py.before'
$patched = $false
$success = $false
Push-Location $root
try {
  $env:PYTHONDONTWRITEBYTECODE = '1'
  $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
  $branch = (git branch --show-current).Trim()
  if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') { throw 'R4G requires develop branch.' }
  $head = (git rev-parse HEAD).Trim()
  if ($LASTEXITCODE -ne 0) { throw 'R4G cannot determine Git HEAD.' }
  Write-Host "R4G_GIT_HEAD=$head"
  $oldTracked = @(git diff --name-only)
  if ($LASTEXITCODE -ne 0) { throw 'R4G cannot read tracked changes.' }
  python -m phase169_r4g_hopf_reference.apply
  if ($LASTEXITCODE -ne 0) { throw 'R4G patch validation or application failed.' }
  $patched = $true
  python -m pytest -q `
    (Join-Path $PSScriptRoot 'tests\test_r4g_patch_safety.py') `
    (Join-Path $PSScriptRoot 'tests\test_r4g_hopf_reference.py') `
    (Join-Path $root 'phase165_r52_r27_r5_typed_references\test_r5_typed_references.py') `
    (Join-Path $root 'phase169_r4e_citation_binding\tests\test_r4e_citation_binding.py') `
    (Join-Path $root 'phase169_r4f_prop44_hopf_application_display\tests\test_r4f_hopf_application.py') `
    (Join-Path $root 'phase169_r4c_pi64_suspension_iso\tests\test_r4c_pi64_suspension_iso.py') `
    (Join-Path $root 'phase169_r3z_reference_only_generic_eta\tests\test_r3z_reference_only_generic_eta.py')
  if ($LASTEXITCODE -ne 0) { throw 'R4G focused pytest failed.' }
  python -m phase169_r4g_hopf_reference.audit
  if ($LASTEXITCODE -ne 0) { throw 'R4G narrative audit failed.' }
  $afterTracked = @(git diff --name-only)
  if ($LASTEXITCODE -ne 0) { throw 'R4G cannot verify tracked changes.' }
  $allowed = @('phase165_r52_r27_r5_literature.py','phase168_r3_37c_reference_projection.py')
  $newChanged = @($afterTracked | Where-Object { $_ -notin $oldTracked -and $_ -notin $allowed })
  if ($newChanged.Count -gt 0) { throw ('R4G unexpected tracked changes: ' + ($newChanged -join ', ')) }
  $success = $true
  Write-Host 'R4G_PRODUCTION_FILES_CHANGED=phase165_r52_r27_r5_literature.py,phase168_r3_37c_reference_projection.py'
  Write-Host 'R4G_FULL_PYTEST_RUN=False'
  Write-Host "R4G_REPORT=$(Join-Path $PSScriptRoot 'output\audit.md')"
} finally {
  if ($patched -and -not $success -and (Test-Path $beforeA) -and (Test-Path $beforeB)) {
    [System.IO.File]::WriteAllBytes($targetA, [System.IO.File]::ReadAllBytes($beforeA))
    [System.IO.File]::WriteAllBytes($targetB, [System.IO.File]::ReadAllBytes($beforeB))
    Write-Host 'R4G_ROLLBACK_APPLIED=True'
  }
  Pop-Location
}

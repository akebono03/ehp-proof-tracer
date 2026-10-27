$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$patched = $false
$success = $false
$files = @('phase168_r3_37c_reference_projection.py', 'phase168_r3_5_model_renderer.py')
Push-Location $root
try {
  $env:PYTHONDONTWRITEBYTECODE = '1'
  $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
  $branch = (git branch --show-current).Trim()
  if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') { throw 'R4E requires develop branch.' }
  $head = (git rev-parse HEAD).Trim()
  if ($LASTEXITCODE -ne 0) { throw 'R4E cannot inspect Git HEAD.' }
  Write-Host "R4E_GIT_BRANCH=$branch"
  Write-Host "R4E_GIT_HEAD=$head"
  $before = @((git diff --name-only) | Sort-Object)
  if ($LASTEXITCODE -ne 0) { throw 'R4E cannot inspect prior tracked differences.' }

  python -m phase169_r4e_citation_binding.patch
  if ($LASTEXITCODE -ne 0) { throw 'R4E patch failed.' }
  $patched = $true

  python -m pytest -q `
    (Join-Path $PSScriptRoot 'tests\test_r4e_patch_safety.py') `
    (Join-Path $PSScriptRoot 'tests\test_r4e_citation_binding.py') `
    (Join-Path $root 'phase169_r4d_pi64_narrative_audit\tests\test_r4d_narrative_audit.py') `
    (Join-Path $root 'phase169_r4c_pi64_suspension_iso\tests\test_r4c_pi64_suspension_iso.py') `
    (Join-Path $root 'phase169_r3z_reference_only_generic_eta\tests\test_r3z_reference_only_generic_eta.py')
  if ($LASTEXITCODE -ne 0) { throw 'R4E focused pytest failed.' }

  python -m phase169_r4e_citation_binding.audit
  if ($LASTEXITCODE -ne 0) { throw 'R4E source-tag audit failed.' }

  $after = @((git diff --name-only) | Sort-Object)
  if ($LASTEXITCODE -ne 0) { throw 'R4E cannot inspect final tracked differences.' }
  $expected = @(($before + $files) | Sort-Object -Unique)
  if (($after -join "`n") -ne ($expected -join "`n")) {
    Write-Host "R4E_EXPECTED_TRACKED_CHANGES=$($expected -join ',')"
    Write-Host "R4E_ACTUAL_TRACKED_CHANGES=$($after -join ',')"
    throw 'R4E changed tracked files outside approved scope.'
  }
  $success = $true
  Write-Host 'R4E_PRODUCTION_FILES_CHANGED=phase168_r3_37c_reference_projection.py,phase168_r3_5_model_renderer.py'
  Write-Host 'R4E_FULL_PYTEST_RUN=False'
  Write-Host "R4E_REPORT=$(Join-Path $PSScriptRoot 'output\audit.md')"
} finally {
  if ($patched -and -not $success) {
    foreach ($file in $files) {
      $old = Join-Path $PSScriptRoot ("output\" + $file + '.before')
      if (Test-Path $old) {
        [System.IO.File]::WriteAllBytes((Join-Path $root $file), [System.IO.File]::ReadAllBytes($old))
      }
    }
    Write-Host 'R4E_ROLLBACK_APPLIED=True'
  }
  Pop-Location
}

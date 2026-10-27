$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$target = Join-Path $root 'phase168_r3_5_model_renderer.py'
$backup = Join-Path $PSScriptRoot 'output\phase168_r3_5_model_renderer.py.before'
$patched = $false
$success = $false
Push-Location $root
try {
  $env:PYTHONDONTWRITEBYTECODE = '1'
  $env:PYTEST_ADDOPTS = '-p no:cacheprovider'
  $branch = (git branch --show-current).Trim()
  if ($LASTEXITCODE -ne 0 -or $branch -ne 'develop') {
    throw 'R4F requires develop branch.'
  }
  $head = (git rev-parse HEAD).Trim()
  if ($LASTEXITCODE -ne 0) { throw 'R4F cannot read Git HEAD.' }
  Write-Host "R4F_GIT_BRANCH=$branch"
  Write-Host "R4F_GIT_HEAD=$head"
  $before = @(git diff --name-only | Sort-Object)
  if ($LASTEXITCODE -ne 0) { throw 'R4F cannot inspect initial Git diff.' }

  Write-Host 'R4F1_FIX=SOURCE_TEX_AND_R4E_NARRATIVE_REGRESSION'
  python -m phase169_r4f_prop44_hopf_application_display.patch
  if ($LASTEXITCODE -ne 0) { throw 'R4F patch failed safely.' }
  $patched = $true

  python -m pytest -q `
    (Join-Path $PSScriptRoot 'tests\test_r4f_patch_safety.py') `
    (Join-Path $PSScriptRoot 'tests\test_r4f_hopf_application.py') `
    (Join-Path $root 'phase169_r4e_citation_binding\tests\test_r4e_citation_binding.py') `
    (Join-Path $root 'phase169_r4e_citation_binding\tests\test_r4e_patch_safety.py') `
    (Join-Path $root 'phase169_r4d_pi64_narrative_audit\tests\test_r4d_narrative_audit.py') `
    (Join-Path $root 'phase169_r4c_pi64_suspension_iso\tests\test_r4c_pi64_suspension_iso.py') `
    (Join-Path $root 'phase169_r3z_reference_only_generic_eta\tests\test_r3z_reference_only_generic_eta.py')
  if ($LASTEXITCODE -ne 0) { throw 'R4F focused pytest failed.' }

  python -m phase169_r4f_prop44_hopf_application_display.audit
  if ($LASTEXITCODE -ne 0) { throw 'R4F proof narrative audit failed.' }

  $after = @(git diff --name-only | Sort-Object)
  if ($LASTEXITCODE -ne 0) { throw 'R4F cannot inspect final Git diff.' }
  $expected = @(($before + @('phase168_r3_5_model_renderer.py')) | Sort-Object -Unique)
  if (($after -join "`n") -ne ($expected -join "`n")) {
    Write-Host "R4F_EXPECTED_TRACKED_CHANGES=$($expected -join ',')"
    Write-Host "R4F_ACTUAL_TRACKED_CHANGES=$($after -join ',')"
    throw 'R4F unexpected tracked file changes.'
  }
  $success = $true
  Write-Host 'R4F_PRODUCTION_FILES_CHANGED=phase168_r3_5_model_renderer.py'
  Write-Host 'R4F_FULL_PYTEST_RUN=False'
  Write-Host "R4F_REPORT=$(Join-Path $PSScriptRoot 'output\audit.md')"
} finally {
  if ($patched -and -not $success -and (Test-Path $backup)) {
    [System.IO.File]::WriteAllBytes($target, [System.IO.File]::ReadAllBytes($backup))
    Write-Host 'R4F_ROLLBACK_APPLIED=True'
  }
  Pop-Location
}

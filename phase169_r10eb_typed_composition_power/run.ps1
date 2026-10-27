$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
$base = 'dcd86c8588b4a667105f16617e0972fc559405c1'
$reviewed = @{
  'phase168_r3_27_typed_statement_projection.py' = 'acc1ba15d78872553921dc30fd7487e4a48e89d2'
  'toda_human_readable_renderer.py' = '2eb51eac89684310ecebd41ac09afc8f8ae0eb61'
  'phase169_r10b_registered_stable_family_binding/family_registry.py' = '4e461795954cc3e7a34fe9e3b47f77d00e5faeda'
  'data/HyoujiGen.csv' = '26f33db0c83ba7f151433583fe861598399cbe6a'
  'phase168_r3_5_model_renderer.py' = 'd4d0aa6b3973d5c3d6fe88861cf11948c419cd6b'
  'phase168_r3_41p13_trust_boundary/verification.py' = '547464846ce574d227092a4aacb895d2e2dfefca'
}
$targets = @('phase168_r3_27_typed_statement_projection.py', 'toda_human_readable_renderer.py')
$before = @{}
$outputBefore = @{}
$snapshotted = $false
$previousLocation = Get-Location
try {
  Set-Location $root
  $env:PYTHONDONTWRITEBYTECODE = '1'
  $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
  $env:PYTEST_ADDOPTS = ''
  $branch = (& git branch --show-current).Trim()
  $head = (& git rev-parse HEAD).Trim()
  Write-Output "R10EB_BRANCH=$branch"
  Write-Output "R10EB_HEAD=$head"
  Write-Output "R10EB_REVIEWED_ANCESTOR=$base"
  if ($branch -ne 'develop') { throw 'R10EB requires develop branch' }
  & git merge-base --is-ancestor $base HEAD
  if ($LASTEXITCODE -ne 0) { throw 'R10EB refused: HEAD is not a descendant of reviewed commit' }
  foreach ($path in @($reviewed.Keys)) {
    $blob = (& git rev-parse "HEAD:$path").Trim()
    if ($LASTEXITCODE -ne 0 -or $blob -ne $reviewed[$path]) {
      throw "R10EB refused: reviewed source changed $path"
    }
  }
  foreach ($path in $targets) {
    & git diff --quiet HEAD -- $path
    if ($LASTEXITCODE -ne 0) { throw "R10EB refused: existing local modifications to $path" }
    & git diff --cached --quiet HEAD -- $path
    if ($LASTEXITCODE -ne 0) { throw "R10EB refused: staged local modifications to $path" }
  }
  # Existing verified proof families are prerequisites; no mathematical patch is made.
  $eta = [IO.File]::ReadAllText((Join-Path $root 'phase165_r12_r21_eta_generator_chain.py'))
  $family = [IO.File]::ReadAllText((Join-Path $root 'phase169_r10d2_general_family_definition/family_citation.py'))
  $shared = [IO.File]::ReadAllText((Join-Path $root 'phase165_r52_r9_shared_math.py'))
  if (-not $eta.Contains('_matching_eta_name(goal.source_generator, older.element)')) {
    throw 'R10EB requires R10E9 verified eta alias implementation'
  }
  if (-not $family.Contains('CHAPTER_VI_SOURCE_RECORDS') -or -not $shared.Contains('build_cited_chapter_vi_family_definitions')) {
    throw 'R10EB requires R10E8 verified cited family implementation'
  }
  Write-Output 'R10EB_REVIEWED_BLOBS=PASS'
  $trackedBefore = @(& git diff --name-only)
  $outputNames = @(
    'audit.json',
    'pi_22_13.md', 'pi_23_15.md', 'pi_24_15.md', 'pi_39_30.md',
    'phase168_r3_27_typed_statement_projection.py.FULL',
    'phase168_r3_27_typed_statement_projection.py.FUNCTION_FULL.py',
    'toda_human_readable_renderer.py.FULL',
    'toda_human_readable_renderer.py.FUNCTION_FULL.py'
  )
  $outputFolder = Join-Path $folder 'output'
  foreach ($path in $targets) {
    $before[$path] = [IO.File]::ReadAllBytes((Join-Path $root $path))
  }
  foreach ($name in $outputNames) {
    $path = Join-Path $outputFolder $name
    $outputBefore[$path] = if (Test-Path -LiteralPath $path) { [IO.File]::ReadAllBytes($path) } else { $null }
  }
  $snapshotted = $true
  Write-Output 'R10EB_SCOPE=TYPED_PRESENTATION_ONLY'
  & python -B -m phase169_r10eb_typed_composition_power.patch
  if ($LASTEXITCODE -ne 0) { throw 'R10EB guarded display patch failed' }
  & python -B -m pytest -q -p no:cacheprovider `
    'phase169_r10eb_typed_composition_power/tests/test_r10eb_typed_composition_power.py' `
    'phase169_r10eb_typed_composition_power/tests/test_r10eb_offline_guards.py' `
    'phase169_r10eb_typed_composition_power/tests/test_r10eb_offline_display.py' `
    'phase166_r3av_sigma_power/test_sigma_power.py' `
    'phase166_r3as_registered_generator_latex/test_r3as.py' `
    'phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py' `
    'phase169_r10e9_eta_composite_alias_fix/tests/test_r10e9_eta_composite_alias.py' `
    'phase169_r10ea_direct_sum_narrative_audit/tests/test_r10ea_audit.py'
  if ($LASTEXITCODE -ne 0) { throw 'R10EB focused pytest failed' }
  & python -B -m phase169_r10eb_typed_composition_power.audit
  if ($LASTEXITCODE -ne 0) { throw 'R10EB typed public/narrative audit failed' }
  $trackedAfter = @(& git diff --name-only)
  $expected = @($trackedBefore) + @($targets) | Select-Object -Unique
  $unexpected = @($trackedAfter | Where-Object { $_ -notin $expected })
  if ($unexpected.Count -gt 0) { throw ('R10EB unexpected tracked changes: ' + ($unexpected -join ',')) }
  $missing = @($trackedBefore | Where-Object { $_ -notin $trackedAfter })
  if ($missing.Count -gt 0) { throw ('R10EB previous tracked changes lost: ' + ($missing -join ',')) }
  foreach ($path in $targets) {
    if ($path -notin $trackedAfter) { throw "R10EB expected patch not observed $path" }
  }
  Write-Output ('R10EB_PRODUCTION_FILES_CHANGED=' + ($targets -join ','))
  Write-Output 'R10EB_INFERENCE_ENGINE_CHANGED=False'
  Write-Output 'R10EB_FULL_PYTEST_RUN=False'
  Write-Output 'R10EB_FOCUSED_TESTS_AND_AUDIT=PASS'
  Write-Output 'R10EB_INTEGRITY=PASS'
}
catch {
  if ($snapshotted) {
    foreach ($path in $before.Keys) {
      [IO.File]::WriteAllBytes((Join-Path $root $path), $before[$path])
    }
    foreach ($path in $outputBefore.Keys) {
      if ($null -eq $outputBefore[$path]) {
        if (Test-Path -LiteralPath $path) { Remove-Item -LiteralPath $path -Force }
      } else {
        [IO.File]::WriteAllBytes($path, $outputBefore[$path])
      }
    }
    Write-Output 'R10EB_ROLLBACK=tracked sources and known outputs restored'
  }
  Write-Output ('R10EB_FAILURE=' + $_.Exception.Message)
  exit 1
}
finally { Set-Location $previousLocation }

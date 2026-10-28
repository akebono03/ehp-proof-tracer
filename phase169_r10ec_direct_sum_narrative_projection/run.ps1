$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
$base = 'b80a8475051b384fb0c58b21d2b74980caccc4e0'
$reviewed = @{
  'phase168_r3_5_model_renderer.py' = 'd4d0aa6b3973d5c3d6fe88861cf11948c419cd6b'
  'phase168_r3_41p13_trust_boundary/verification.py' = '547464846ce574d227092a4aacb895d2e2dfefca'
  'phase169_r10e1_general_group_transport/transport.py' = 'd60770fff1b6e14791db6b952733f4062a64c8eb'
  'phase169_r10a_verified_stable_chain_projection/projection.py' = 'c387b6a46d71561f8ecc2f2dc1d78158145dd883'
  'phase168_r3_29_order_projection.py' = 'b0eaf673fa0d36a31a6831b1297679b48453d8a8'
  'phase168_r3_4_link_bridge.py' = 'c3a6233a57c41e61e6649ee33c7a336d7aa1c664'
}
$target = 'phase168_r3_5_model_renderer.py'
$before = $null
$outputBefore = @{}
$snapshotted = $false
$previous = Get-Location
try {
  Set-Location $root
  $env:PYTHONDONTWRITEBYTECODE = '1'
  $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
  $env:PYTEST_ADDOPTS = ''
  $branch = (& git branch --show-current).Trim()
  $head = (& git rev-parse HEAD).Trim()
  Write-Output "R10EC_BRANCH=$branch"
  Write-Output "R10EC_HEAD=$head"
  Write-Output "R10EC_REVIEWED_ANCESTOR=$base"
  if ($branch -ne 'develop') { throw 'R10EC requires develop branch' }
  & git merge-base --is-ancestor $base HEAD
  if ($LASTEXITCODE -ne 0) { throw 'R10EC HEAD does not descend from reviewed base' }
  foreach ($path in @($reviewed.Keys)) {
    $blob = (& git rev-parse "HEAD:$path").Trim()
    if ($LASTEXITCODE -ne 0 -or $blob -ne $reviewed[$path]) {
      throw "R10EC reviewed Git source changed: $path"
    }
  }
  & git diff --quiet HEAD -- $target
  if ($LASTEXITCODE -ne 0) { throw 'R10EC refused: local renderer modifications exist' }
  & git diff --cached --quiet HEAD -- $target
  if ($LASTEXITCODE -ne 0) { throw 'R10EC refused: staged renderer modifications exist' }
  # R10EB is a required verified local display change; never silently reapply it.
  $typed = [IO.File]::ReadAllText((Join-Path $root 'phase168_r3_27_typed_statement_projection.py'))
  $public = [IO.File]::ReadAllText((Join-Path $root 'toda_human_readable_renderer.py'))
  if (-not $typed.Contains('typed_stable_composition_power_latex') -or -not $public.Contains('typed_stable_composition_power_latex')) {
    throw 'R10EC requires applied R10EB typed power display'
  }
  Write-Output 'R10EC_REVIEWED_BLOBS_AND_R10EB_PRECONDITIONS=PASS'
  $trackedBefore = @(& git diff --name-only)
  $outdir = Join-Path $folder 'output'
  $outputNames = @('audit.json', 'phase168_r3_5_model_renderer.py.FULL',
                   'render_model_backed_narrative_markdown_FULL.py',
                   'pi_22_13.md', 'pi_23_15.md', 'pi_24_15.md', 'pi_39_30.md')
  $before = [IO.File]::ReadAllBytes((Join-Path $root $target))
  foreach ($name in $outputNames) {
    $path = Join-Path $outdir $name
    $outputBefore[$path] = if (Test-Path -LiteralPath $path) {
      [IO.File]::ReadAllBytes($path)
    } else { $null }
  }
  $snapshotted = $true
  Write-Output 'R10EC_SCOPE=VERIFIED_DIRECT_SUM_PRESENTATION_ONLY'
  & python -B -m phase169_r10ec_direct_sum_narrative_projection.patch
  if ($LASTEXITCODE -ne 0) { throw 'R10EC guarded renderer patch failed' }
  & python -B -m pytest -q -p no:cacheprovider `
    'phase169_r10ec_direct_sum_narrative_projection/tests/test_r10ec_patch.py' `
    'phase169_r10ec_direct_sum_narrative_projection/tests/test_r10ec_projection.py' `
    'phase169_r10a_verified_stable_chain_projection/tests/test_r10a_verified_stable_chain.py' `
    'phase169_r10eb_typed_composition_power/tests/test_r10eb_typed_composition_power.py' `
    'phase169_r10ea_direct_sum_narrative_audit/tests/test_r10ea_audit.py'
  if ($LASTEXITCODE -ne 0) { throw 'R10EC focused pytest failed' }
  & python -B -m phase169_r10ec_direct_sum_narrative_projection.audit
  if ($LASTEXITCODE -ne 0) { throw 'R10EC proof/narrative audit failed' }
  $trackedAfter = @(& git diff --name-only)
  $expected = @($trackedBefore) + @($target) | Select-Object -Unique
  $unexpected = @($trackedAfter | Where-Object { $_ -notin $expected })
  if ($unexpected.Count -gt 0) { throw ('R10EC unexpected tracked diff: ' + ($unexpected -join ',')) }
  $missing = @($trackedBefore | Where-Object { $_ -notin $trackedAfter })
  if ($missing.Count -gt 0) { throw ('R10EC prior changes disappeared: ' + ($missing -join ',')) }
  if ($target -notin $trackedAfter) { throw 'R10EC renderer patch missing from git diff' }
  Write-Output "R10EC_PRODUCTION_FILES_CHANGED=$target"
  Write-Output 'R10EC_PROOF_TREE_UNCHANGED=True'
  Write-Output 'R10EC_FULL_PYTEST_RUN=False'
  Write-Output 'R10EC_FOCUSED_TESTS_AND_AUDIT=PASS'
  Write-Output 'R10EC_INTEGRITY=PASS'
}
catch {
  if ($snapshotted) {
    [IO.File]::WriteAllBytes((Join-Path $root $target), $before)
    foreach ($path in @($outputBefore.Keys)) {
      if ($null -eq $outputBefore[$path]) {
        if (Test-Path -LiteralPath $path) { Remove-Item -LiteralPath $path -Force }
      } else {
        [IO.File]::WriteAllBytes($path, $outputBefore[$path])
      }
    }
    Write-Output 'R10EC_ROLLBACK=renderer and known outputs restored byte-for-byte'
  }
  Write-Output ('R10EC_FAILURE=' + $_.Exception.Message)
  exit 1
}
finally {
  Set-Location $previous
}

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
$reviewedAncestor = 'f486c3680990066e45d97ca1948654c1eb9ca539'
$projectionExpectedSha256 = '53c20a8c3911866de7da44f31df1a965e333d5a4961ab215918637334ec686e0'
$reviewedBlobs = @{
  'phase165_r55_nk_only_goal.py' = 'b207b8169590e634229d412324d857ffb3857939'
  'phase168_r3_41p13_trust_boundary/verification.py' = '547464846ce574d227092a4aacb895d2e2dfefca'
  'phase169_r10e1_general_group_transport/transport.py' = 'd60770fff1b6e14791db6b952733f4062a64c8eb'
  'phase168_r3_29_order_projection.py' = 'b0eaf673fa0d36a31a6831b1297679b48453d8a8'
  'phase168_r3_4_link_bridge.py' = 'c3a6233a57c41e61e6649ee33c7a336d7aa1c664'
}
$previous = Get-Location
try {
  Set-Location $root
  $env:PYTHONDONTWRITEBYTECODE = '1'
  $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
  $env:PYTEST_ADDOPTS = ''
  $branch = (& git branch --show-current).Trim()
  $head = (& git rev-parse HEAD).Trim()
  Write-Output "R10ED_BRANCH=$branch"
  Write-Output "R10ED_HEAD=$head"
  Write-Output "R10ED_REVIEWED_ANCESTOR=$reviewedAncestor"
  Write-Output 'R10ED_MODE=AUDIT_ONLY'
  if ($branch -ne 'develop') { throw 'R10ED requires the local develop branch' }
  & git merge-base --is-ancestor $reviewedAncestor HEAD
  if ($LASTEXITCODE -ne 0) { throw 'R10ED HEAD is not descended from reviewed main' }
  foreach ($entry in $reviewedBlobs.GetEnumerator()) {
    $blob = (& git rev-parse "HEAD:$($entry.Key)").Trim()
    if ($LASTEXITCODE -ne 0 -or $blob -ne $entry.Value) {
      throw "R10ED reviewed Git dependency changed: $($entry.Key)"
    }
  }
  Write-Output 'R10ED_GITHUB_REVIEWED_DEPENDENCIES=PASS'
  $projection = Join-Path $root 'phase169_r10ec_direct_sum_narrative_projection\projection.py'
  $renderer = Join-Path $root 'phase168_r3_5_model_renderer.py'
  if (-not (Test-Path -LiteralPath $projection) -or -not (Test-Path -LiteralPath $renderer)) {
    throw 'R10ED requires the already applied R10EC projection and renderer'
  }
  $digest = (Get-FileHash -LiteralPath $projection -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($digest -ne $projectionExpectedSha256) {
    throw 'R10ED requires the exact reviewed R10EC projection; production drift detected'
  }
  $rendererBody = [IO.File]::ReadAllText($renderer)
  if (-not $rendererBody.Contains('project_verified_direct_sum_transport(model, order)')) {
    throw 'R10ED requires previously applied R10EC renderer wiring'
  }
  $r10ecTest = Join-Path $root 'phase169_r10ec_direct_sum_narrative_projection\tests\test_r10ec_projection.py'
  if (-not (Test-Path -LiteralPath $r10ecTest) -or
      -not ([IO.File]::ReadAllText($r10ecTest)).Contains('n=8, k=2')) {
    throw 'R10ED requires R10EC-R1 corrected cyclic regression test'
  }
  Write-Output 'R10ED_R10EC_AND_R10ECR1_PRECONDITIONS=PASS'
  $trackedBefore = (& git status --porcelain --untracked-files=no | Out-String)
  $rendererBefore = (Get-FileHash -LiteralPath $renderer -Algorithm SHA256).Hash
  $projectionBefore = (Get-FileHash -LiteralPath $projection -Algorithm SHA256).Hash
  & python -B -m pytest -q -p no:cacheprovider `
    'phase169_r10ed_direct_sum_generality_audit/tests/test_r10ed_profile.py' `
    'phase169_r10ed_direct_sum_generality_audit/tests/test_r10ed_projection_refusal.py' `
    'phase169_r10ec_direct_sum_narrative_projection/tests/test_r10ec_projection.py' `
    'phase169_r10a_verified_stable_chain_projection/tests/test_r10a_verified_stable_chain.py'
  if ($LASTEXITCODE -ne 0) { throw 'R10ED focused tests failed' }
  & python -B -m phase169_r10ed_direct_sum_generality_audit.audit
  if ($LASTEXITCODE -ne 0) { throw 'R10ED generality audit failed' }
  $trackedAfter = (& git status --porcelain --untracked-files=no | Out-String)
  if ($trackedBefore -cne $trackedAfter) { throw 'R10ED unexpectedly changed tracked files' }
  if ($rendererBefore -ne (Get-FileHash -LiteralPath $renderer -Algorithm SHA256).Hash) {
    throw 'R10ED unexpectedly changed renderer bytes'
  }
  if ($projectionBefore -ne (Get-FileHash -LiteralPath $projection -Algorithm SHA256).Hash) {
    throw 'R10ED unexpectedly changed projection bytes'
  }
  Write-Output 'R10ED_TRACKED_FILES_UNCHANGED=PASS'
  Write-Output 'R10ED_INTEGRITY=PASS'
  Write-Output 'R10ED_FULL_PYTEST_RUN=False'
  Write-Output 'R10ED_LIMITED_TESTS_AND_AUDIT=PASS'
}
catch {
  Write-Output ('R10ED_FAILURE=' + $_.Exception.Message)
  Write-Output 'R10ED_PRODUCTION_FILES_CHANGED=none'
  exit 1
}
finally {
  Set-Location $previous
}

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
$testRel = 'phase169_r10ec_direct_sum_narrative_projection/tests/test_r10ec_projection.py'
$testPath = Join-Path $root $testRel
$originalRunner = Join-Path $root 'phase169_r10ec_direct_sum_narrative_projection/run.ps1'
$knownTestHash = '2bec8d3cc27d6ebcd496468b4576dc9c9e48ffe7301f5c9a8da22b8cf588d713'
$knownRunnerHash = '7c2800c40b181d31995dd301a63afbc9cf25729801ea14413d541a24f7167dae'
$outputDir = Join-Path $folder 'output'
$outputNames = @('test_r10ec_projection.py.FULL',
  'test_r10ec_cyclic_non_direct_sum_is_not_compressed_FULL.py',
  'test_r10ec_projection_IMPORTS_FULL.py')
$originalTest = $null
$originalOutputs = @{}
$backedUp = $false
$previous = Get-Location
try {
  Set-Location $root
  $env:PYTHONDONTWRITEBYTECODE = '1'
  $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
  $branch = (& git branch --show-current).Trim()
  $head = (& git rev-parse HEAD).Trim()
  Write-Output "R10ECR1_BRANCH=$branch"
  Write-Output "R10ECR1_HEAD=$head"
  Write-Output 'R10ECR1_SCOPE=FOCUSED_TEST_ALIGNMENT_ONLY'
  if ($branch -ne 'develop') { throw 'R10ECR1 requires develop branch' }
  & git merge-base --is-ancestor 'f486c3680990066e45d97ca1948654c1eb9ca539' HEAD
  if ($LASTEXITCODE -ne 0) { throw 'R10ECR1 HEAD does not descend from reviewed merge' }
  $blob = (& git rev-parse 'HEAD:phase168_r3_5_model_renderer.py').Trim()
  if ($LASTEXITCODE -ne 0 -or $blob -ne 'd4d0aa6b3973d5c3d6fe88861cf11948c419cd6b') {
    throw 'R10ECR1 renderer Git blob is no longer reviewed'
  }
  if (-not (Test-Path -LiteralPath $originalRunner)) { throw 'R10EC original runner not found' }
  if (-not (Test-Path -LiteralPath $testPath)) { throw 'R10EC original focused test not found' }
  $testHash = (Get-FileHash -LiteralPath $testPath -Algorithm SHA256).Hash.ToLowerInvariant()
  $runnerHash = (Get-FileHash -LiteralPath $originalRunner -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($testHash -ne $knownTestHash) { throw 'R10ECR1 test has unexpected contents; do not overwrite it' }
  if ($runnerHash -ne $knownRunnerHash) { throw 'R10ECR1 original R10EC runner changed' }
  & git diff --quiet HEAD -- 'phase168_r3_5_model_renderer.py'
  if ($LASTEXITCODE -ne 0) { throw 'R10ECR1 renderer has uncommitted changes' }
  $originalTest = [IO.File]::ReadAllBytes($testPath)
  foreach ($name in $outputNames) {
    $file = Join-Path $outputDir $name
    $originalOutputs[$file] = if (Test-Path -LiteralPath $file) {
      [IO.File]::ReadAllBytes($file)
    } else { $null }
  }
  $backedUp = $true
  & python -B -m pytest -q -p no:cacheprovider `
    'phase169_r10ecr1_cyclic_test_alignment/tests/test_r10ecr1_patch.py'
  if ($LASTEXITCODE -ne 0) { throw 'R10ECR1 guard tests failed' }
  & python -B -m phase169_r10ecr1_cyclic_test_alignment.patch
  if ($LASTEXITCODE -ne 0) { throw 'R10ECR1 guarded focused test patch failed' }
  & powershell -NoProfile -ExecutionPolicy Bypass -File $originalRunner
  if ($LASTEXITCODE -ne 0) { throw 'R10ECR1 original R10EC focused tests/audit failed' }
  Write-Output 'R10ECR1_PRODUCTION_PATCH_DELEGATED_TO_ORIGINAL_R10EC=True'
  Write-Output 'R10ECR1_TEST_PATCHED_ONLY=phase169_r10ec_direct_sum_narrative_projection/tests/test_r10ec_projection.py'
  Write-Output 'R10ECR1_FULL_PYTEST_RUN=False'
  Write-Output 'R10ECR1_LIMITED_TESTS_AND_AUDIT=PASS'
}
catch {
  if ($backedUp) {
    [IO.File]::WriteAllBytes($testPath, $originalTest)
    foreach ($file in @($originalOutputs.Keys)) {
      if ($null -eq $originalOutputs[$file]) {
        if (Test-Path -LiteralPath $file) { Remove-Item -LiteralPath $file -Force }
      } else {
        [IO.File]::WriteAllBytes($file, $originalOutputs[$file])
      }
    }
    Write-Output 'R10ECR1_ROLLBACK=focused test and outputs restored byte-for-byte'
  }
  Write-Output ('R10ECR1_FAILURE=' + $_.Exception.Message)
  exit 1
}
finally {
  Set-Location $previous
}

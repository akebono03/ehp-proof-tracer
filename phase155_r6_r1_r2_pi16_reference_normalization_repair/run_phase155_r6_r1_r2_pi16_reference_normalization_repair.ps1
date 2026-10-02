$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$R6Package = Join-Path `
  $RepoRoot `
  "phase155_r6_pytest_collection_runtime_audit"
$R6Audit = Join-Path `
  $R6Package `
  "audit_phase155_r6.py"

Write-Host "=============================================================="
Write-Host "Phase 155-R6-R1-R2 - pi16 reference normalization repair"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "This repair is LIGHTWEIGHT."
Write-Host "The 21 collection batches will NOT be repeated."
Write-Host "The 26-second Phase144 repaired test will NOT be repeated."
Write-Host "Only the remaining pi16_9 test is changed and run."
Write-Host ""

if (-not (Test-Path $R6Audit)) {
  throw "Required R6 audit package not found: $R6Audit"
}

Write-Host "1/4 Lightweight R2 tooling tests"

python -m pytest `
  "$PackageDir\test_phase155_r6_r1_r2_tools.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "R6-R1-R2 tooling tests failed."
}

Write-Host ""
Write-Host "2/4 Apply one-function stale expectation repair"

python `
  "$PackageDir\repair_phase155_r6_r1_r2.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "R6-R1-R2 repair failed."
}

python `
  "$PackageDir\verify_phase155_r6_r1_r2.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "R6-R1-R2 source verification failed."
}

Write-Host ""
Write-Host "3/4 Run only the remaining pi16_9 test"

$FocusedTest = (
  "tests/test_phase150_rc4_7a_cross_group_reference_normalization.py" +
  "::test_phase150_rc4_7a_pi16_9_numbers_normalized_references"
)

python -m pytest `
  $FocusedTest `
  -q `
  --durations=5 `
  --durations-min=0.0 `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "R6-R1-R2 focused pi16_9 test failed."
}

Write-Host ""
Write-Host "4/4 Replace only the two stale FAIL runtime checkpoints, then resume R6"

$RuntimeCheckpointDir = Join-Path `
  $RepoRoot `
  "phase155_r6_audit_output\runtime_checkpoints"

$FailedCheckpoints = @()

Get-ChildItem `
  -Path $RuntimeCheckpointDir `
  -Filter "*.json" |
ForEach-Object {
  $Payload = Get-Content `
    $_.FullName `
    -Raw |
    ConvertFrom-Json

  if ($Payload.status -eq "FAIL") {
    $FailedCheckpoints += $_.FullName
  }
}

Write-Host "saved FAIL checkpoints: $($FailedCheckpoints.Count)"

if ($FailedCheckpoints.Count -ne 2) {
  throw "Expected exactly 2 saved FAIL checkpoints; found $($FailedCheckpoints.Count)."
}

foreach ($Checkpoint in $FailedCheckpoints) {
  Write-Host "remove failed checkpoint: $Checkpoint"
  Remove-Item `
    $Checkpoint `
    -Force
}

Write-Host ""
Write-Host "Resume R6 with checkpoint reuse."
Write-Host "Expected:"
Write-Host "  collect 1-21: checkpoint PASS - skip"
Write-Host "  runtime 1-8: checkpoint PASS - skip"
Write-Host "  runtime 9-10: re-run"
Write-Host "  runtime 11-12: checkpoint PASS - skip"
Write-Host ""

python `
  "$R6Audit" `
  --repo-root "$RepoRoot" `
  --runtime-timeout 60

if ($LASTEXITCODE -ne 0) {
  throw "R6 resume still has a failure."
}

Write-Host ""
Write-Host "Phase 155-R6-R1-R2 completed."
Write-Host "Production changes: none"
Write-Host "Additional existing-test change: 1 function"
Write-Host "Canonical regression: NOT run"
Write-Host "Repository-wide pytest: NOT run"

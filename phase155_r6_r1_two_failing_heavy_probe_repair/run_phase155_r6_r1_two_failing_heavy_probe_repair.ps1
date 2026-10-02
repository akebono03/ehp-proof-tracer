$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$R6Package = Join-Path $RepoRoot "phase155_r6_pytest_collection_runtime_audit"
$R6Audit = Join-Path $R6Package "audit_phase155_r6.py"

Write-Host "=============================================================="
Write-Host "Phase 155-R6-R1 - two failing heavy probes repair"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "This repair is LIGHTWEIGHT."
Write-Host "The 21 collection batches will NOT be repeated."
Write-Host "The 10 already-passing runtime probes will NOT be repeated."
Write-Host "Only the two failing test expectations are changed and re-run."
Write-Host ""

if (-not (Test-Path $R6Audit)) {
  throw "Required R6 audit package not found: $R6Audit"
}

Write-Host "1/5 Lightweight unit tests for R6-R1 tooling"
python -m pytest `
  "$PackageDir\test_phase155_r6_r1_tools.py" `
  -q `
  -p no:cacheprovider
if ($LASTEXITCODE -ne 0) {
  throw "R6-R1 tooling tests failed."
}

Write-Host ""
Write-Host "2/5 Diagnose the two saved FAIL checkpoints"
python `
  "$PackageDir\repair_phase155_r6_r1.py" `
  --repo-root "$RepoRoot" `
  --diagnostic-only
if ($LASTEXITCODE -ne 0) {
  throw "R6-R1 checkpoint diagnosis did not match the expected two failures."
}

Write-Host ""
Write-Host "3/5 Apply minimal stale-expectation repair"
python `
  "$PackageDir\repair_phase155_r6_r1.py" `
  --repo-root "$RepoRoot"
if ($LASTEXITCODE -ne 0) {
  throw "R6-R1 expectation repair failed."
}

python `
  "$PackageDir\verify_phase155_r6_r1.py" `
  --repo-root "$RepoRoot"
if ($LASTEXITCODE -ne 0) {
  throw "R6-R1 source verification failed."
}

Write-Host ""
Write-Host "4/5 Run only the two repaired tests"

$FocusedTests = @(
  "tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py::test_phase144_6_r5_43_11_all_selected_contributions_are_insertable_and_rendered",
  "tests/test_phase150_rc4_7a_cross_group_reference_normalization.py::test_phase150_rc4_7a_pi16_9_numbers_normalized_references"
)

python -m pytest `
  @FocusedTests `
  -q `
  --durations=10 `
  --durations-min=0.0 `
  -p no:cacheprovider
if ($LASTEXITCODE -ne 0) {
  throw "R6-R1 focused repaired tests failed."
}

Write-Host ""
Write-Host "5/5 Remove only the two FAIL runtime checkpoints and resume R6"

$RuntimeCheckpointDir = Join-Path `
  $RepoRoot `
  "phase155_r6_audit_output\runtime_checkpoints"

$Removed = 0

Get-ChildItem `
  -Path $RuntimeCheckpointDir `
  -Filter "*.json" |
ForEach-Object {
  $Payload = Get-Content `
    $_.FullName `
    -Raw |
    ConvertFrom-Json

  if ($Payload.status -eq "FAIL") {
    Write-Host "remove failed checkpoint: $($_.Name)"
    Remove-Item $_.FullName -Force
    $Removed += 1
  }
}

if ($Removed -ne 2) {
  throw "Expected to remove exactly 2 failed runtime checkpoints; removed $Removed."
}

Write-Host ""
Write-Host "Resuming R6."
Write-Host "Expected:"
Write-Host "  collection 1-21: checkpoint PASS - skip"
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
Write-Host "Phase 155-R6-R1 completed."
Write-Host "Production changes: none"
Write-Host "Changed existing test files: 2"
Write-Host "Canonical regression: NOT run"
Write-Host "Repository-wide pytest: NOT run"

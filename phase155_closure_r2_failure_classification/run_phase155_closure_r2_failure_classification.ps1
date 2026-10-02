$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$LogPath = Join-Path `
  $RepoRoot `
  "phase155_closure_output\phase155_full_pytest.log"

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2 - 98 failure classification"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "This run is LIGHTWEIGHT."
Write-Host "The 10,421-test repository suite will NOT run."
Write-Host "No heavy Phase144 or Phase95-98 test will run."
Write-Host "Production code will NOT change."
Write-Host "Repository tests will NOT change."
Write-Host ""

if (-not (Test-Path $LogPath)) {
  throw "Closure full-suite log not found: $LogPath"
}

Write-Host "1/2 Lightweight classifier self-tests"

python -m pytest `
  "$PackageDir\test_phase155_closure_r2_audit.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2 classifier self-tests failed."
}

Write-Host ""
Write-Host "2/2 Classify the saved 98 full-suite failures"

python `
  "$PackageDir\phase155_closure_r2_audit.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R2 classification failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R2 classification COMPLETE"
Write-Host "=============================================================="
Write-Host "Expected result:"
Write-Host "  SAFE_STALE: 38"
Write-Host "  HISTORICAL_HEAVY: 36"
Write-Host "  CONTRACT_SENSITIVE: 24"
Write-Host "  UNKNOWN: 0"
Write-Host ""
Write-Host "No repository test bodies were executed."
Write-Host "No production files were changed."
Write-Host ""
Write-Host "Report:"
Write-Host "  $RepoRoot\phase155_closure_r2_output\phase155_closure_r2_classification.md"
Write-Host ""
Write-Host "Next:"
Write-Host "  repair SAFE_STALE with focused tests only;"
Write-Host "  then review HISTORICAL_HEAVY and CONTRACT_SENSITIVE separately."

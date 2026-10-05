$ErrorActionPreference = "Stop"

$PhaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PhaseDir

Write-Host "=============================================================="
Write-Host "Phase 158-R5-5c-1 - finding classification"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host ""

Push-Location $RepoRoot
try {
  Write-Host "[1/2] Run lightweight classifier tests"
  python -m pytest `
    ".\phase158_r5_5c_1_finding_classification\test_phase158_r5_5c_1_classifier.py" `
    -q

  Write-Host ""
  Write-Host "[2/2] Classify the 5 R5-5c findings"
  python ".\phase158_r5_5c_1_finding_classification\audit_phase158_r5_5c_1.py"
}
finally {
  Pop-Location
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 158-R5-5c-1 classification complete"
Write-Host "No production code was changed."
Write-Host "No repository-wide pytest was run."
Write-Host "=============================================================="

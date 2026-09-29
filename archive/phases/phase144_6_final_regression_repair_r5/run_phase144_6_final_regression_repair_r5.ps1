$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$SourceTest = Join-Path $PatchRoot "tests\test_phase143_15_argument_ordering.py"
$TargetTest = Join-Path $ProjectRoot "tests\test_phase143_15_argument_ordering.py"

Write-Host "=============================================================="
Write-Host "Phase 144-6 Final Regression Repair R5"
Write-Host "Phase 143 argument-ordering test identity-contract repair"
Write-Host "Production code changes: none"
Write-Host "Persistent test changes: tests/test_phase143_15_argument_ordering.py"
Write-Host "=============================================================="

if (-not (Test-Path $TargetTest)) {
  throw "Target test file not found: $TargetTest"
}

Copy-Item -Path $SourceTest -Destination $TargetTest -Force
Write-Host ""
Write-Host "Applied:"
Write-Host "  tests/test_phase143_15_argument_ordering.py"

$env:PYTHONPATH = $ProjectRoot

try {
  Write-Host ""
  Write-Host "Running focused pi_16^9 regression..."
  pytest -q `
    "tests/test_phase143_15_argument_ordering.py::test_phase143_15_pi16_9_definition_precedes_group_structure"

  if ($LASTEXITCODE -ne 0) {
    throw "Focused pi_16^9 regression failed."
  }

  Write-Host ""
  Write-Host "Running complete Phase 143-15 argument-ordering tests..."
  pytest -q `
    "tests/test_phase143_15_argument_ordering.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase 143-15 argument-ordering tests failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 144-6 Final Regression Repair R5 focused tests: PASS"
  Write-Host "No full-suite run is performed by this repair runner."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}

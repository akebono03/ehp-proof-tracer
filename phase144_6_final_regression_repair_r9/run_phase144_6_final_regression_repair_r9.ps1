$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$SourceTest = Join-Path $PatchRoot "tests\test_phase143_15_argument_ordering.py"
$TargetTest = Join-Path $ProjectRoot "tests\test_phase143_15_argument_ordering.py"
$TemporaryPackageMarker = Join-Path $ProjectRoot "tests\__init__.py"
$CreatedTemporaryPackageMarker = $false

Write-Host "=============================================================="
Write-Host "Phase 144-6 Final Regression Repair R9"
Write-Host "pi_16^9 stale structural test-contract repair"
Write-Host "Production code changes: none"
Write-Host "Persistent test changes: tests/test_phase143_15_argument_ordering.py"
Write-Host "=============================================================="

if (-not (Test-Path $TargetTest)) {
  throw "Target test file not found: $TargetTest"
}

Copy-Item `
  -Path $SourceTest `
  -Destination $TargetTest `
  -Force

if (-not (Test-Path $TemporaryPackageMarker)) {
  New-Item `
    -Path $TemporaryPackageMarker `
    -ItemType File `
    -Force | Out-Null
  $CreatedTemporaryPackageMarker = $true
  Write-Host "Temporary package marker created: tests/__init__.py"
}

$env:PYTHONPATH = "$ProjectRoot;$ProjectRoot\tests"

try {
  Write-Host ""
  Write-Host "Running focused pi_16^9 ordering regression..."
  pytest -q `
    "tests/test_phase143_15_argument_ordering.py::test_phase143_15_pi16_9_definition_precedes_group_structure"

  if ($LASTEXITCODE -ne 0) {
    throw "Focused pi_16^9 ordering regression failed."
  }

  Write-Host ""
  Write-Host "Running complete Phase 143-15 ordering tests..."
  pytest -q `
    "tests/test_phase143_15_argument_ordering.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase 143-15 ordering tests failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 144-6 Final Regression Repair R9 focused tests: PASS"
  Write-Host "Production behavior was not changed."
  Write-Host "Full suite is intentionally not run by this repair runner."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue

  if ($CreatedTemporaryPackageMarker) {
    Remove-Item `
      $TemporaryPackageMarker `
      -Force `
      -ErrorAction SilentlyContinue
    Write-Host "Temporary package marker removed: tests/__init__.py"
  }
}

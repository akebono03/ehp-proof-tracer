$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

$PreviousPythonPath = $env:PYTHONPATH

if ([string]::IsNullOrWhiteSpace($PreviousPythonPath)) {
  $env:PYTHONPATH = $RepoRoot
}
else {
  $env:PYTHONPATH = "$RepoRoot;$PreviousPythonPath"
}

try {
  Write-Host "=============================================================="
  Write-Host "Phase 159 R1-7c R4 repair9 runner fix1"
  Write-Host "final reflexive suppression + post-selection Reference relink"
  Write-Host "=============================================================="
  Write-Host "Repository root: $RepoRoot"
  Write-Host "PYTHONPATH includes repository root."
  Write-Host ""

  Write-Host "[1/5] Pre-apply targeted audit"
  python ".\phase159_r1_7c_r4_repair9_runner_fix1\audit_phase159_r1_7c_r4_repair9.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Pre-apply audit failed."
  }

  Write-Host ""
  Write-Host "[2/5] Apply production repair"
  python ".\phase159_r1_7c_r4_repair9_runner_fix1\apply_phase159_r1_7c_r4_repair9.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Production repair failed."
  }

  Write-Host ""
  Write-Host "[3/5] Run repair9 focused tests"
  python -m pytest -q `
    ".\phase159_r1_7c_r4_repair9_runner_fix1\test_phase159_r1_7c_r4_repair9.py" `
    ".\tests\test_phase157_r20_repair30_final_reflexive_suppression.py" `
    ".\tests\test_phase157_r20_repair53_r3c_legacy_reference_marker_remapping.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Focused tests failed."
  }

  Write-Host ""
  Write-Host "[4/5] Run directly affected contract tests"
  python -m pytest -q `
    ".\tests\test_phase157_r20_repair12_map_property_reference_support.py" `
    ".\tests\test_phase158_r5_5b_public_generic_order_route.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Directly affected contract tests failed."
  }

  Write-Host ""
  Write-Host "[5/5] Post-apply targeted audit"
  python ".\phase159_r1_7c_r4_repair9_runner_fix1\audit_phase159_r1_7c_r4_repair9.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Post-apply audit failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "repair9 focused verification completed."
  Write-Host "Repository-wide pytest was NOT run."
  Write-Host "=============================================================="
}
finally {
  $env:PYTHONPATH = $PreviousPythonPath
}

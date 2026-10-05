$ErrorActionPreference = "Stop"

function Assert-LastExitCode {
  param(
    [string]$Step
  )

  if ($LASTEXITCODE -ne 0) {
    throw "$Step failed with exit code $LASTEXITCODE"
  }
}

Write-Host "=============================================================="
Write-Host "Phase 158-R3 - stale boundary repair5"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $PackageDir "..")).Path

Set-Location $RepoRoot

Write-Host "[1/4] Apply test-only repair"
python `
  ".\phase158_r3_stale_boundary_repair5_remove_brittle_start\apply_phase158_r3_stale_boundary_repair5.py"
Assert-LastExitCode "apply repair5"

Write-Host "[2/4] Run repaired Phase 156 boundary tests"
python -m pytest `
  ".\tests\test_phase156_r5_repair9_test_contract_after_boundary_collapse.py::test_phase156_r5_repair9_depth2_public_body_starts_after_53_boundary" `
  ".\tests\test_phase156_r5_repair9_test_contract_after_boundary_collapse.py::test_phase156_r5_repair9_depth3_public_body_starts_after_53_boundary" `
  -q
Assert-LastExitCode "repaired boundary tests"

Write-Host "[3/4] Re-run stale intro contract audit"
python `
  ".\phase158_r3_stale_intro_tests_repair2_local_adaptive\audit_phase158_r3_stale_intro_tests_repair2.py"
Assert-LastExitCode "stale intro contract audit"

Write-Host "[4/4] Re-run Phase 158-R3 112-group audit"
python `
  ".\phase158_r3_reference_intro_normalization\audit_phase158_r3.py"
Assert-LastExitCode "Phase 158-R3 112-group audit"

Write-Host "=============================================================="
Write-Host "Phase 158-R3 stale boundary repair5 complete candidate."
Write-Host "Production code changes: none"
Write-Host "Full repository pytest: NOT run"
Write-Host "=============================================================="

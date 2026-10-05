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
Write-Host "Phase 158-R3 - stale intro tests repair2 (local-adaptive)"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $PackageDir "..")).Path

Set-Location $RepoRoot

Write-Host "[1/4] Detect and repair only local stale intro contracts"
python `
  ".\phase158_r3_stale_intro_tests_repair2_local_adaptive\apply_phase158_r3_stale_intro_tests_repair2.py"
Assert-LastExitCode "local-adaptive test-only repair"

Write-Host "[2/4] Run only affected test functions"
python `
  ".\phase158_r3_stale_intro_tests_repair2_local_adaptive\run_modified_intro_tests.py"
Assert-LastExitCode "affected test functions"

Write-Host "[3/4] Audit remaining stale intro contracts"
python `
  ".\phase158_r3_stale_intro_tests_repair2_local_adaptive\audit_phase158_r3_stale_intro_tests_repair2.py"
Assert-LastExitCode "stale intro contract audit"

Write-Host "[4/4] Re-run Phase 158-R3 112-group audit"
python `
  ".\phase158_r3_reference_intro_normalization\audit_phase158_r3.py"
Assert-LastExitCode "Phase 158-R3 112-group audit"

Write-Host "=============================================================="
Write-Host "Phase 158-R3 stale intro repair2 complete candidate."
Write-Host "Production code changes: none"
Write-Host "Full repository pytest: NOT run"
Write-Host "=============================================================="

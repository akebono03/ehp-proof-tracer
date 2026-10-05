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
Write-Host "Phase 158-R3 - Reference intro normalization"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $PackageDir "..")).Path

Set-Location $RepoRoot

Write-Host "[1/4] Apply Phase 158-R3"
python `
  ".\phase158_r3_reference_intro_normalization\apply_phase158_r3.py"
Assert-LastExitCode "apply Phase 158-R3"

Write-Host "[2/4] Focused Phase 158-R3 tests"
python -m pytest `
  ".\phase158_r3_reference_intro_normalization\test_phase158_r3_reference_intro_normalization.py" `
  -q
Assert-LastExitCode "focused Phase 158-R3 tests"

Write-Host "[3/4] 112-group Reference intro audit"
python `
  ".\phase158_r3_reference_intro_normalization\audit_phase158_r3.py"
Assert-LastExitCode "112-group Reference intro audit"

Write-Host "[4/4] Show summary"
Get-Content `
  ".\phase158_r3_reference_intro_normalization\output\phase158_r3_summary.txt" `
  -Encoding UTF8

Write-Host "=============================================================="
Write-Host "Phase 158-R3 complete candidate."
Write-Host "Full repository pytest: NOT run"
Write-Host "Known stale tests that require old intro wording: NOT run"
Write-Host "=============================================================="

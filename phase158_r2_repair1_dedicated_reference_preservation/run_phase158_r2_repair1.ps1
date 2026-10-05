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
Write-Host "Phase 158-R2 repair1 - dedicated Reference preservation"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $PackageDir "..")).Path

Set-Location $RepoRoot

Write-Host "[1/4] Apply repair1"
python `
  ".\phase158_r2_repair1_dedicated_reference_preservation\apply_phase158_r2_repair1.py"
Assert-LastExitCode "apply repair1"

Write-Host "[2/4] Focused tests"
python -m pytest `
  ".\phase158_r2_repair1_dedicated_reference_preservation\test_phase158_r2_repair1.py" `
  ".\tests\test_phase134_26_narrative_shell.py" `
  ".\tests\test_phase134_24_pi15_8_narrative.py" `
  ".\tests\test_phase150_rc4_7a_cross_group_reference_normalization.py" `
  -q
Assert-LastExitCode "focused tests"

Write-Host "[3/4] 112-group contract + dedicated preservation audit"
python `
  ".\phase158_r2_repair1_dedicated_reference_preservation\audit_phase158_r2_repair1.py"
Assert-LastExitCode "112-group audit"

Write-Host "[4/4] Show summary"
Get-Content `
  ".\phase158_r2_repair1_dedicated_reference_preservation\output\phase158_r2_repair1_summary.txt" `
  -Encoding UTF8

Write-Host "=============================================================="
Write-Host "Phase 158-R2 repair1 complete."
Write-Host "Full repository pytest: NOT run"
Write-Host "=============================================================="

$ErrorActionPreference = "Stop"

function Assert-LastExitCode {
  param(
    [string]$Label
  )

  if ($LASTEXITCODE -ne 0) {
    throw "$Label failed with exit code $LASTEXITCODE"
  }
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 158-R5-5a - Public depth=2 audit parity repair"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production code changes: none"
Write-Host ""

Write-Host "[1/3] Focused audit tests"
python -m pytest `
  ".\phase158_r5_5a_public_depth2_audit_parity_repair\test_phase158_r5_5a.py" `
  -q
Assert-LastExitCode "focused audit tests"

Write-Host ""
Write-Host "[2/3] Public depth=2 parity audit"
python `
  ".\phase158_r5_5a_public_depth2_audit_parity_repair\audit_phase158_r5_5a.py"
Assert-LastExitCode "public depth=2 parity audit"

Write-Host ""
Write-Host "[3/3] Show audit details"
Get-Content `
  ".\phase158_r5_5a_public_depth2_audit_parity_repair\audit_output\details.txt"

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 158-R5-5a complete"
Write-Host "No repository-wide pytest was run."
Write-Host "Next boundary: classify confirmed ordering defects for R5-5b."
Write-Host "=============================================================="

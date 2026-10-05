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
Write-Host "Phase 158-R5-5b repair1v - Web verification fix"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host ""

Write-Host "[1/2] Run lightweight Web verification"
python -m pytest `
  ".\phase158_r5_5b_repair1v_web_verification_fix\test_phase158_r5_5b_repair1v_web_verification.py" `
  -q
Assert-LastExitCode "lightweight Web verification"

Write-Host ""
Write-Host "[2/2] Show public Web proof bodies"
python `
  ".\phase158_r5_5b_repair1v_web_verification_fix\show_phase158_r5_5b_repair1v_web.py"
Assert-LastExitCode "public Web proof bodies"

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 158-R5-5b repair1v Web verification complete"
Write-Host "No production code was changed."
Write-Host "No repository-wide pytest was run."
Write-Host "=============================================================="

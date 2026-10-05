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
Write-Host "Phase 158-R5-5c - generic public ordering cross-audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host ""

Write-Host "[1/2] Run lightweight audit-harness tests"
python -m pytest `
  ".\phase158_r5_5c_cross_group_generic_order_audit\test_phase158_r5_5c.py" `
  -q
Assert-LastExitCode "audit-harness tests"

Write-Host ""
Write-Host "[2/2] Run current-corpus Web Narrative ordering audit"
python `
  ".\phase158_r5_5c_cross_group_generic_order_audit\audit_phase158_r5_5c.py"
Assert-LastExitCode "R5-5c cross-audit"

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 158-R5-5c audit complete"
Write-Host "No production code was changed."
Write-Host "No repository-wide pytest was run."
Write-Host "=============================================================="

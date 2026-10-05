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
$OutputDir = Join-Path $ScriptDir "audit_output"

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 158-R5-5a repair3a - runner output-directory fix"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production code changes: none"
Write-Host "Diagnosis code changes: none"
Write-Host ""

Write-Host "[1/4] Ensure audit output directory"
New-Item `
  -ItemType Directory `
  -Path $OutputDir `
  -Force `
  | Out-Null

Write-Host ""
Write-Host "[2/4] Focused diagnosis tests"
python -m pytest `
  ".\phase158_r5_5a_repair3_ordering_ownership_diagnosis\test_phase158_r5_5a_repair3.py" `
  -q
Assert-LastExitCode "focused diagnosis tests"

Write-Host ""
Write-Host "[3/4] Run ordering ownership diagnosis"
python `
  ".\phase158_r5_5a_repair3_ordering_ownership_diagnosis\audit_phase158_r5_5a_repair3.py" `
  *> `
  ".\phase158_r5_5a_repair3_ordering_ownership_diagnosis\audit_output\console.txt"
Assert-LastExitCode "ordering ownership diagnosis"

Write-Host ""
Write-Host "[4/4] Show compact targets"
Write-Host ""
Write-Host "--- pi7_4 ---"
Get-Content `
  ".\phase158_r5_5a_repair3_ordering_ownership_diagnosis\audit_output\pi7_4.txt"

Write-Host ""
Write-Host "--- pi15_8 ---"
Get-Content `
  ".\phase158_r5_5a_repair3_ordering_ownership_diagnosis\audit_output\pi15_8.txt"

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 158-R5-5a repair3a complete"
Write-Host "No production code was changed."
Write-Host "No repository-wide pytest was run."
Write-Host "=============================================================="

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
Write-Host "Phase 158-R5-5b repair1q - contract runtime source diagnosis"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production code changes: none"
Write-Host ""

Write-Host "[1/3] Ensure audit output directory"
New-Item `
  -ItemType Directory `
  -Path $OutputDir `
  -Force `
  | Out-Null

Write-Host ""
Write-Host "[2/3] Run lightweight diagnosis test"
python -m pytest `
  ".\phase158_r5_5b_repair1q_contract_runtime_source_diagnosis\test_phase158_r5_5b_repair1q.py" `
  -q
Assert-LastExitCode "lightweight diagnosis test"

Write-Host ""
Write-Host "[3/3] Run contract runtime-source diagnosis"
python `
  ".\phase158_r5_5b_repair1q_contract_runtime_source_diagnosis\audit_phase158_r5_5b_repair1q.py"
Assert-LastExitCode "contract runtime-source diagnosis"

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 158-R5-5b repair1q diagnosis complete"
Write-Host "No production code was changed."
Write-Host "No repository-wide pytest was run."
Write-Host "=============================================================="

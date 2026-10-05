$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 158-R5-4 repair1 - audit runner path fix"
Write-Host "=============================================================="

$AuditDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $AuditDir

Set-Location $RepoRoot

Write-Host "[1/4] Confirm R5-3 route marker in current production source"
$source = Get-Content `
  ".\toda_group_proof_narrative_renderer.py" `
  -Raw

if ($source -notmatch "if presentation\.max_depth >= 2:") {
  throw "R5-3 common-route change was not found in current source."
}

Write-Host "[2/4] Remove previous audit output"
Remove-Item `
  "$AuditDir\audit_output" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Write-Host "[3/4] Run audit-only renderer inspection"
python "$AuditDir\audit_phase158_r5_4.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 158-R5-4 audit failed with exit code $LASTEXITCODE."
}

Write-Host "[4/4] Show summary"
$summaryPath = "$AuditDir\audit_output\summary.txt"

if (-not (Test-Path $summaryPath)) {
  throw "Audit summary was not created: $summaryPath"
}

Get-Content $summaryPath

Write-Host ""
Write-Host "No production code was changed."
Write-Host "No test code was changed."
Write-Host "pytest was intentionally not run."
Write-Host ""
Write-Host "Please paste summary.txt and, if findings are nonzero, details.txt."

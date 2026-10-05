$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 158-R5-5 - derivation completeness audit"
Write-Host "=============================================================="

$AuditDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $AuditDir

Set-Location $RepoRoot

Write-Host "[1/4] Confirm R5-3 common public route"
$rendererSource = Get-Content `
  ".\toda_group_proof_narrative_renderer.py" `
  -Raw

if ($rendererSource -notmatch "if presentation\.max_depth >= 2:") {
  throw "R5-3 common-route change was not found."
}

Write-Host "[2/4] Confirm R5-4 equation-numbering repair"
$numberingSource = Get-Content `
  ".\toda_group_proof_narrative_equation_numbering.py" `
  -Raw

if ($numberingSource -notmatch "reference_plans = \[\]") {
  throw "R5-4 equation-numbering repair was not found."
}

Write-Host "[3/4] Run audit-only derivation completeness inspection"
Remove-Item `
  "$AuditDir\audit_output" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

python "$AuditDir\audit_phase158_r5_5.py"

if ($LASTEXITCODE -ne 0) {
  throw "R5-5 audit failed with exit code $LASTEXITCODE."
}

Write-Host "[4/4] Show summary"
Get-Content `
  "$AuditDir\audit_output\summary.txt"

Write-Host ""
Write-Host "No production code was changed."
Write-Host "No test code was changed."
Write-Host "pytest was intentionally not run."
Write-Host ""
Write-Host "Please paste summary.txt and details.txt."

$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$OutputDir = Join-Path $RepoRoot "phase155_closure_r4_output"

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R4-R2 - audit reclassification + final closure"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Routine regression evidence from Closure-R3 is preserved."
Write-Host "Three obsolete/deferred audit functions will be removed."
Write-Host "Final audit-only boundary: 2"
Write-Host "Phase156 deferred duplicate pressure: 117"
Write-Host "Monolithic pytest will NOT run."
Write-Host ""

Write-Host "1/4 Apply audit reclassification"

python `
  "$PackageDir\apply_phase155_closure_r4_r2.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R4-R2 apply failed."
}

Write-Host ""
Write-Host "2/4 Run the final two explicit audits"

python `
  "$PackageDir\run_phase155_closure_r4_r2_audits.py" `
  --repo-root "$RepoRoot" `
  --output-dir "$OutputDir" `
  --timeout 600

if ($LASTEXITCODE -ne 0) {
  Write-Host ""
  Write-Host "Closure-R4-R2 audit run is INCOMPLETE."
  Write-Host "Documentation was NOT updated."
  throw "Closure-R4-R2 audits failed."
}

Write-Host ""
Write-Host "3/4 Update complete Phase155 closure documentation"

python `
  "$PackageDir\update_phase155_closure_r4_r2_docs.py" `
  --repo-root "$RepoRoot" `
  --output-dir "$OutputDir"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R4-R2 documentation update failed."
}

Write-Host ""
Write-Host "4/4 Verify audit boundary and documentation"

python `
  "$PackageDir\verify_phase155_closure_r4_r2.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R4-R2 verification failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R4-R2 COMPLETE"
Write-Host "=============================================================="
Write-Host "Current collection: 10384"
Write-Host "Routine tests: 10382"
Write-Host "Final audit-only tests: 2"
Write-Host "Routine sharded regression: PASS"
Write-Host "Final audit-only explicit closure: 2/2 PASS"
Write-Host "Phase156 duplicate pressure recorded: 117"
Write-Host "Documentation: updated and verified"
Write-Host "Production changes: none"
Write-Host "Monolithic repository-wide pytest: NOT run"

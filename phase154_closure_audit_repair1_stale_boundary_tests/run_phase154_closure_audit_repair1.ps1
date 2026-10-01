$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir
$ClosureAuditRunner = Join-Path `
  $RepoRoot `
  "phase154_closure_audit\run_phase154_closure_audit.ps1"

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154 Closure Audit Repair1 - Stale Boundary Tests"
Write-Host "=============================================================================="
Write-Host "Production changes: none"
Write-Host ""

python ".\phase154_closure_audit_repair1_stale_boundary_tests\apply_phase154_closure_audit_repair1.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154 closure audit Repair1 apply failed."
}

if (-not (Test-Path $ClosureAuditRunner)) {
  throw "Original Phase 154 closure audit runner is missing: $ClosureAuditRunner"
}

Write-Host ""
Write-Host "Re-run Phase 154 closure audit from the beginning:"
powershell -ExecutionPolicy Bypass `
  -File $ClosureAuditRunner

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154 closure audit Repair1 re-run failed."
}

Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154 Closure Audit Repair1 completed"
Write-Host "=============================================================================="
Write-Host "Production changes: none"
Write-Host "Full test suite: NOT RUN (reserved for phase end)"

$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R5-R5 - 112-group cross-audit re-audit"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "Repository root: $RepoRoot"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host "Pytest: not run"
Write-Host "Full Narrative rendering: not used"
Write-Host ""

python "$PackageDir\audit_phase157_r5_r5.py"
$AuditExitCode = $LASTEXITCODE

Write-Host ""
if ($AuditExitCode -eq 0) {
  Write-Host "Phase157-R5-R5 audit completed with PASS."
} else {
  Write-Host "Phase157-R5-R5 audit completed with NEEDS REVIEW."
}

Write-Host "Repository-wide pytest is intentionally deferred to Phase157 closure."

exit $AuditExitCode

$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$OutputDir = Join-Path $RepoRoot "phase155_closure_r3_output"

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R3-R3 - final job1 stale-contract repair"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "R3-R2 jobs 2-8 are preserved as PASS."
Write-Host "Only the three former job1 failures are repaired/verified."
Write-Host "Audit-only tests will NOT run."
Write-Host "Monolithic pytest will NOT run."
Write-Host ""

Write-Host "1/2 Apply minimal stale-contract repair"

python `
  "$PackageDir\apply_phase155_closure_r3_r3.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R3-R3 apply failed."
}

Write-Host ""
Write-Host "2/2 Verify only the three repaired contracts"

python `
  "$PackageDir\verify_phase155_closure_r3_r3.py" `
  --repo-root "$RepoRoot" `
  --output-dir "$OutputDir"

if ($LASTEXITCODE -ne 0) {
  throw "Closure-R3-R3 focused verification failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R3-R3 COMPLETE"
Write-Host "=============================================================="
Write-Host "Closure-R3 routine result: PASS"
Write-Host "Audit-only tests executed: 0"
Write-Host "Monolithic repository-wide pytest: NOT run"

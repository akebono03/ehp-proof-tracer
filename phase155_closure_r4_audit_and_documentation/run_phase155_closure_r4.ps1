$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$OutputDir = Join-Path $RepoRoot "phase155_closure_r4_output"

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R4 - audit-only closure + documentation"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Policy:"
Write-Host "  validate exact audit-only manifest: 5 nodeids"
Write-Host "  collect current tests"
Write-Host "  run audit-only tests one by one"
Write-Host "  checkpoint PASS audits"
Write-Host "  update documentation only after 5/5 PASS"
Write-Host "  monolithic repository-wide pytest: NOT run"
Write-Host ""

Write-Host "1/3 Current collection + explicit audit-only closure"

python `
  "$PackageDir\run_phase155_closure_r4_audits.py" `
  --repo-root "$RepoRoot" `
  --output-dir "$OutputDir" `
  --timeout-seconds 600

if ($LASTEXITCODE -ne 0) {
  Write-Host ""
  Write-Host "Closure-R4 audit-only closure is INCOMPLETE."
  Write-Host "PASS audits remain checkpointed."
  Write-Host "Documentation was NOT updated."
  throw "Phase155 Closure-R4 audit-only run failed."
}

Write-Host ""
Write-Host "2/3 Write complete Phase155 closure documentation"

python `
  "$PackageDir\update_phase155_closure_docs.py" `
  --repo-root "$RepoRoot" `
  --output-dir "$OutputDir"

if ($LASTEXITCODE -ne 0) {
  throw "Phase155 Closure-R4 documentation update failed."
}

Write-Host ""
Write-Host "3/3 Verify documentation boundary"

python `
  "$PackageDir\verify_phase155_closure_docs.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase155 Closure-R4 documentation verification failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R4 COMPLETE"
Write-Host "=============================================================="
Write-Host "Routine sharded regression: PASS (Closure-R3)"
Write-Host "Audit-only explicit closure: 5/5 PASS"
Write-Host "Documentation: updated and verified"
Write-Host "Production changes: none"
Write-Host "Monolithic repository-wide pytest: NOT run"
Write-Host ""
Write-Host "Full documentation copies:"
Write-Host "  $OutputDir\documentation"

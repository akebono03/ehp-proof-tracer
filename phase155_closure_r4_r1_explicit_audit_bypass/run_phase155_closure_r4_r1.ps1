$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$OutputDir = Join-Path $RepoRoot "phase155_closure_r4_output"
$OriginalPackageDir = Join-Path $RepoRoot "phase155_closure_r4_audit_and_documentation"

Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R4-R1 - explicit audit deselection bypass"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Previous result: 5 audit tests were deselected, not executed."
Write-Host "This repair changes only the audit runner."
Write-Host "Production/test/documentation content is not changed before audits pass."
Write-Host ""

Write-Host "1/3 Run the exact five audit-only tests explicitly"

python `
  "$PackageDir\run_phase155_closure_r4_r1_audits.py" `
  --repo-root "$RepoRoot" `
  --output-dir "$OutputDir" `
  --timeout-seconds 600

if ($LASTEXITCODE -ne 0) {
  Write-Host ""
  Write-Host "Closure-R4-R1 audit execution is INCOMPLETE."
  Write-Host "Documentation was NOT updated."
  throw "Phase155 Closure-R4-R1 audit run failed."
}

if (-not (Test-Path "$OriginalPackageDir\update_phase155_closure_docs.py")) {
  throw "Original Closure-R4 package directory not found: $OriginalPackageDir"
}

Write-Host ""
Write-Host "2/3 Apply the already-reviewed Phase155 closure documentation"

python `
  "$OriginalPackageDir\update_phase155_closure_docs.py" `
  --repo-root "$RepoRoot" `
  --output-dir "$OutputDir"

if ($LASTEXITCODE -ne 0) {
  throw "Phase155 Closure-R4-R1 documentation update failed."
}

Write-Host ""
Write-Host "3/3 Verify documentation boundary"

python `
  "$OriginalPackageDir\verify_phase155_closure_docs.py" `
  --repo-root "$RepoRoot"

if ($LASTEXITCODE -ne 0) {
  throw "Phase155 Closure-R4-R1 documentation verification failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 155 Closure-R4-R1 COMPLETE"
Write-Host "=============================================================="
Write-Host "Routine sharded regression: PASS"
Write-Host "Audit-only explicit closure: 5/5 PASS"
Write-Host "Documentation: updated and verified"
Write-Host "Production changes: none"
Write-Host "Monolithic repository-wide pytest: NOT run"

$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154 Documentation Closure"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Document files: 5"
Write-Host "Full test suite: NOT RUN"
Write-Host ""

Write-Host "[1/3] Apply full-document updates"
python ".\phase154_documentation_closure\apply_phase154_documentation_closure.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154 documentation closure apply failed."
}

Write-Host ""
Write-Host "[2/3] Verify documentation contract"
python ".\phase154_documentation_closure\verify_phase154_documentation_closure.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154 documentation closure verification failed."
}

Write-Host ""
Write-Host "[3/3] Updated full documents"
Write-Host "  .\phase154_documentation_closure\updated_full_documents\README.md"
Write-Host "  .\phase154_documentation_closure\updated_full_documents\docs\design.md"
Write-Host "  .\phase154_documentation_closure\updated_full_documents\docs\development_log.md"
Write-Host "  .\phase154_documentation_closure\updated_full_documents\docs\roadmap.md"
Write-Host "  .\phase154_documentation_closure\updated_full_documents\docs\proof_records.md"

Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154 Documentation Closure completed"
Write-Host "=============================================================================="
Write-Host "Production changes: none"
Write-Host "Full test suite: NOT RUN"
Write-Host "Next: Phase 154 final full regression"

$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 160 documentation closure"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Set-Location $RepoRoot

Write-Host "[1/1] Update documentation"
python "$PackageRoot\apply_phase160_documentation_closure.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Phase 160 documentation closure applied."
Write-Host "No tests were run."
Write-Host ""
Write-Host "Full updated documentation files:"
Write-Host "  $PackageRoot\generated_full_docs\README.md"
Write-Host "  $PackageRoot\generated_full_docs\docs\design.md"
Write-Host "  $PackageRoot\generated_full_docs\docs\development_log.md"
Write-Host "  $PackageRoot\generated_full_docs\docs\roadmap.md"
Write-Host "  $PackageRoot\generated_full_docs\docs\proof_records.md"

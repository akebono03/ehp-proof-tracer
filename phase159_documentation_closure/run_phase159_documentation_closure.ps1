$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 documentation closure"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Repository root: $RepoRoot"
Write-Host "Package root:    $PackageRoot"
Write-Host ""
Write-Host "This closure package records the Phase 159 documentation boundary."
Write-Host "Before applying documentation changes, confirm that these files are the current repository versions:"
Write-Host "  README.md"
Write-Host "  docs/design.md"
Write-Host "  docs/development_log.md"
Write-Host "  docs/roadmap.md"
Write-Host "  docs/proof_records.md"
Write-Host ""
Write-Host "Phase-final full regression command:"
Write-Host "  python -m pytest -q"
Write-Host ""
Write-Host "No production Python code is changed by this package."

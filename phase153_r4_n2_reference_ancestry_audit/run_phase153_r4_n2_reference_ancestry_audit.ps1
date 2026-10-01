$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "=============================================================="
Write-Host "Phase 153-R4 - 6-group n=2 Reference ancestry audit"
Write-Host "Production changes: none"
Write-Host "=============================================================="

Set-Location $RepoRoot

Write-Host ""
Write-Host "A. Running the six-group Reference ancestry audit..."
python "$PackageDir\audit_phase153_r4_n2_reference_ancestry.py"

Write-Host ""
Write-Host "B. Running the R4 audit-package focused tests..."
python -m pytest -q "$PackageDir\test_phase153_r4_n2_reference_ancestry_audit.py"

Write-Host ""
Write-Host "C. Running existing Reference-focused regression tests..."
python -m pytest -q `
  ".\tests\test_phase144_6_r3_structured_references.py" `
  ".\tests\test_phase144_6_r3_production_references.py"

$Phase153Tests = Get-ChildItem `
  -Path ".\tests" `
  -Filter "test_phase153_*.py" `
  -File `
  -ErrorAction SilentlyContinue

if ($Phase153Tests.Count -gt 0) {
  Write-Host ""
  Write-Host "D. Running locally present Phase 153 focused tests..."
  $Phase153Paths = @(
    $Phase153Tests |
      ForEach-Object {
        $_.FullName
      }
  )
  python -m pytest -q @Phase153Paths
}
else {
  Write-Host ""
  Write-Host "D. No tests\test_phase153_*.py files found; skipping."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 153-R4 audit completed."
Write-Host "Review:"
Write-Host "$PackageDir\output\phase153_r4_n2_reference_ancestry_audit.md"
Write-Host "No production files were modified."
Write-Host "Full pytest is intentionally deferred to the end of Phase 153."
Write-Host "=============================================================="

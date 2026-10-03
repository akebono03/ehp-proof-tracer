$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase156 closure — restore canonical Phase144 pi6 test"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production changes: none"
Write-Host ""

Set-Location $RepoRoot

Write-Host "1/2 Restore canonical test file from HEAD"
python `
  (Join-Path $PackageRoot "restore_canonical_phase144_pi6_test.py")

if ($LASTEXITCODE -ne 0) {
  throw "Canonical Phase144 pi6 test restore failed."
}

Write-Host ""
Write-Host "2/2 Focused regression"
python -m pytest `
  ".\tests\test_phase144_6_pi6_generic_production_route.py" `
  -q `
  --tb=short `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Focused Phase144 pi6 canonical regression failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Focused canonical test repair completed"
Write-Host "=============================================================="
Write-Host "Production changes: none"
Write-Host "Target test file now matches HEAD exactly."
Write-Host ""
Write-Host "Next:"
Write-Host "  rerun Phase156 closure fixed4 for the final full suite."

$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - repair2g fix10g audit"
Write-Host "Runtime equation-normalizer identity and I/O trace"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host "Production code changes: NONE"
Write-Host "Existing test changes: NONE"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/2] Inspect runtime normalizer and trace pi_3^2"
python "$PackageRoot\audit_phase159_pi4_3_repair2g_fix10g.py"
if ($LASTEXITCODE -ne 0) {
  throw "fix10g runtime audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[2/2] Re-run current two pi_3^2 failures"
python -m pytest `
  tests/test_phase159_r1_2_pi3_2_narrative_repair.py::test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically `
  tests/test_phase159_r1_2_pi3_2_narrative_repair.py::test_phase159_r1_5_pi3_2_public_map_property_wording_is_terse `
  -q
$FocusedExit = $LASTEXITCODE

Write-Host ""
Write-Host "=============================================================="
Write-Host "fix10g audit complete"
Write-Host "Focused pytest exit code: $FocusedExit"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="

exit 0

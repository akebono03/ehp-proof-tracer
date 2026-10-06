
$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - repair2g fix10a audit"
Write-Host "pi_3^2 wording / numbering contract audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host "Production code changes: NONE"
Write-Host "Existing test changes: NONE"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/2] Print pi_3^2 current public Narrative and probes"
python "$PackageRoot\audit_phase159_pi4_3_repair2g_fix10a.py"
if ($LASTEXITCODE -ne 0) {
  throw "fix10a pi_3^2 wording audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[2/2] Re-run the two failing pi_3^2 tests"
python -m pytest `
  tests/test_phase159_r1_2_pi3_2_narrative_repair.py::test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically `
  tests/test_phase159_r1_2_pi3_2_narrative_repair.py::test_phase159_r1_5_pi3_2_public_map_property_wording_is_terse `
  -q
$FocusedExit = $LASTEXITCODE

Write-Host ""
Write-Host "=============================================================="
Write-Host "fix10a audit complete"
Write-Host "Focused pytest exit code: $FocusedExit"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="

exit 0

$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 repair2e"
Write-Host "pi_6^3 current-contract audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/3] Run Phase 157 pi_6^3 current Reference contract"
python -m pytest `
  tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py `
  tests/test_phase157_r3_pi6_3_reference_boundary.py `
  -q
$ReferenceExit = $LASTEXITCODE

Write-Host ""
Write-Host "[2/3] Run numbered-derivation current contract"
python -m pytest `
  tests/test_phase143_57c_step_derivation_connector.py `
  tests/test_phase143_61b_r_semantic_suppression_priority.py `
  tests/test_phase144_6_pi6_generic_production_route.py `
  tests/test_phase144_6_r25_9a_pi5_suppression.py `
  tests/test_phase144_6_r25_9a_r1_relocation_hidden.py `
  -q
$NumberingExit = $LASTEXITCODE

Write-Host ""
Write-Host "[3/3] Run Phase 159 repair1 health checks"
python -m pytest `
  tests/test_phase159_pi4_3_prop51_direct_delta_provenance.py `
  tests/test_phase159_pi4_3_repair1c_prop56_direct_prop51_dependency.py `
  -q
$Repair1Exit = $LASTEXITCODE

Write-Host ""
Write-Host "=============================================================="
Write-Host "Contract audit summary"
Write-Host "Phase157 reference contract exit: $ReferenceExit"
Write-Host "Numbered derivation contract exit: $NumberingExit"
Write-Host "Phase159 repair1 health exit: $Repair1Exit"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="

if (
  $Repair1Exit -ne 0
) {
  throw "Phase159 repair1 health checks failed"
}

if (
  $ReferenceExit -eq 0 `
  -and $NumberingExit -eq 0
) {
  Write-Host "AUDIT_RESULT=PASS_NO_REGRESSION"
  exit 0
}

Write-Host "AUDIT_RESULT=CONTRACT_REGRESSION_CONFIRMED"
exit 0

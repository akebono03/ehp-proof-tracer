$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot
$env:PYTHONPATH = $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159-R1-6d repair1 - EOF whitespace fix"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production code changes: none"
Write-Host ""

Write-Host "[1/6] Apply whitespace-only repair"
python ".\phase159_r1_6d_repair1_eof_whitespace_fix\apply_phase159_r1_6d_repair1.py"
if ($LASTEXITCODE -ne 0) {
  throw "R1-6d repair1 apply failed"
}

Write-Host ""
Write-Host "[2/6] Compile changed test"
python -m py_compile `
  ".\tests\test_phase159_r1_6c_source_faithful_reference_linkage.py"
if ($LASTEXITCODE -ne 0) {
  throw "py_compile failed"
}

Write-Host ""
Write-Host "[3/6] Run R1-6d focused tests"
python -m pytest -q `
  ".\tests\test_phase159_r1_6d_specialization_reference_linkage_finalization.py"
if ($LASTEXITCODE -ne 0) {
  throw "R1-6d focused tests failed"
}

Write-Host ""
Write-Host "[4/6] Re-run R1-6a/R1-6b/R1-6c tests"
python -m pytest -q `
  ".\tests\test_phase159_r1_6a_foundational_reference_identity.py" `
  ".\tests\test_phase159_r1_6b_toda51_attribution.py" `
  ".\tests\test_phase159_r1_6c_source_faithful_reference_linkage.py"
if ($LASTEXITCODE -ne 0) {
  throw "R1-6a/R1-6b/R1-6c tests failed"
}

Write-Host ""
Write-Host "[5/6] Re-run Phase 159 focused + related regressions"
python -m pytest -q `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase159_r1_2_hopf_injective_dependency_role.py" `
  ".\tests\test_phase159_r1_2_hopf_isomorphism_dependency_role.py" `
  ".\tests\test_phase157_r2_literature_statement_boundary.py" `
  ".\tests\test_phase157_r5_r3_boundary_catalog_expansion.py" `
  ".\tests\test_phase49_low_dimensional_facts.py" `
  ".\tests\test_phase49_generator_transport.py"
if ($LASTEXITCODE -ne 0) {
  throw "focused/related regressions failed"
}

Write-Host ""
Write-Host "[6/6] git diff --check"
git diff --check
if ($LASTEXITCODE -ne 0) {
  throw "git diff --check failed"
}

Write-Host ""
Write-Host "PASS: Phase 159-R1-6d repair1 verification completed."
Write-Host "Full pytest was NOT run."

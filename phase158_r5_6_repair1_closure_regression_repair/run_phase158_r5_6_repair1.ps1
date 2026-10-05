$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 158-R5-6 repair1 - closure regression repair"
Write-Host "=============================================================="
Write-Host "Repository root: $((Get-Location).Path)"
Write-Host "Repository-wide pytest: intentionally NOT run here"
Write-Host ""

Write-Host "[1/4] Apply minimal production/test repair"
python ".\phase158_r5_6_repair1_closure_regression_repair\apply_phase158_r5_6_repair1.py"
if ($LASTEXITCODE -ne 0) {
  throw "repair1 patch application failed."
}
Write-Host ""

Write-Host "[2/4] Run direct repaired-contract tests"
python -m pytest `
  tests/test_phase157_r5_r10_reference_proof_boundary_qed.py `
  tests/test_phase158_r4_equation_numbering_and_prose.py `
  tests/test_phase158_r5_4_repair_common_equation_numbering.py `
  tests/test_phase150_rc4_7d_3_public_narrative_generic_route.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "direct repaired-contract tests failed."
}
Write-Host ""

Write-Host "[3/4] Run complete Phase 158-R5 focused closure regression"
python -m pytest `
  tests/test_phase134_26_narrative_shell.py `
  tests/test_phase157_r5_r10_reference_proof_boundary_qed.py `
  tests/test_phase158_r5_3_public_narrative_single_route.py `
  tests/test_phase158_r4_equation_numbering_and_prose.py `
  tests/test_phase158_r5_4_repair_common_equation_numbering.py `
  tests/test_phase158_r5_5b_public_generic_order_route.py `
  tests/test_phase150_rc4_7d_3_public_narrative_generic_route.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "Phase 158-R5-6 focused closure regression failed."
}
Write-Host ""

Write-Host "[4/4] Check patch hygiene"
git diff --check
if ($LASTEXITCODE -ne 0) {
  throw "git diff --check failed."
}
Write-Host ""

Write-Host "=============================================================="
Write-Host "Phase 158-R5-6 repair1 verification PASSED"
Write-Host "If all checks above passed, Phase 158-R5 can be closed."
Write-Host "Do NOT run repository-wide pytest until Phase 158 final closure."
Write-Host "=============================================================="

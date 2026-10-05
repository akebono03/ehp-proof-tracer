$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 158-R5-6 - R5 focused regression / closure verification"
Write-Host "=============================================================="

$repo = (Get-Location).Path
Write-Host "Repository root: $repo"
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host "Repository-wide pytest: intentionally NOT run in R5-6"
Write-Host ""

$tests = @(
  "tests/test_phase134_26_narrative_shell.py",
  "tests/test_phase157_r5_r10_reference_proof_boundary_qed.py",
  "tests/test_phase158_r5_3_public_narrative_single_route.py",
  "tests/test_phase158_r4_equation_numbering_and_prose.py",
  "tests/test_phase158_r5_4_repair_common_equation_numbering.py",
  "tests/test_phase158_r5_5b_public_generic_order_route.py",
  "tests/test_phase150_rc4_7d_3_public_narrative_generic_route.py"
)

Write-Host "[1/3] Verify focused test files exist"
foreach ($test in $tests) {
  if (-not (Test-Path $test)) {
    throw "Required focused test file not found: $test"
  }
}
Write-Host "All focused test files found."
Write-Host ""

Write-Host "[2/3] Run Phase 158-R5 focused regression"
python -m pytest @tests -q
if ($LASTEXITCODE -ne 0) {
  throw "Phase 158-R5-6 focused regression failed."
}
Write-Host ""

Write-Host "[3/3] Verify working-tree diff"
git diff --check
if ($LASTEXITCODE -ne 0) {
  throw "git diff --check failed."
}
Write-Host ""

Write-Host "=============================================================="
Write-Host "Phase 158-R5-6 focused verification PASSED"
Write-Host ""
Write-Host "Verified contracts:"
Write-Host "  - public Narrative shell"
Write-Host "  - Reference / Proof boundary"
Write-Host "  - root target -> QED"
Write-Host "  - depth=2 single generic public route"
Write-Host "  - legacy/dedicated route non-use where guarded"
Write-Host "  - common equation numbering"
Write-Host "  - generic proof ordering"
Write-Host "  - Web Narrative depth=2 ordering"
Write-Host "  - representative public/Web generic route regression"
Write-Host ""
Write-Host "If this passes, Phase 158-R5 can be closed."
Write-Host "Do NOT run repository-wide pytest until Phase 158 final closure."
Write-Host "=============================================================="

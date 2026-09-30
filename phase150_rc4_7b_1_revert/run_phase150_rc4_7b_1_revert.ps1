$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 RC4-7B-1 Revert"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Reverting only the RC4-7B-1 frontier experiment..."
python ".\phase150_rc4_7b_1_revert\apply_phase150_rc4_7b_1_revert.py"

Write-Host ""
Write-Host "B. Syntax preflight..."
python -m py_compile ".\toda_group_proof_narrative_arguments.py"

Write-Host ""
Write-Host "C. Focused Argument regressions..."
$existing = @()
$patterns = @(
  ".\tests\test_phase147_rc1_argument_*.py",
  ".\tests\test_phase148_*.py",
  ".\tests\test_phase149_*.py"
)
foreach ($pattern in $patterns) {
  $existing += Get-ChildItem $pattern -ErrorAction SilentlyContinue |
    ForEach-Object { $_.FullName }
}
if ($existing.Count -gt 0) {
  python -m pytest -q $existing
} else {
  Write-Host "No matching focused regression files found."
}

Write-Host ""
Write-Host "D. Confirming the Phase 143 reference regression separately..."
python -m pytest -q `
  ".\tests\test_phase143_46_multi_argument_narrative_assembler.py::test_phase143_46_pi15_8_single_argument_has_no_discourse_marker"

Write-Host ""
Write-Host "=============================================================="
Write-Host "RC4-7B-1 revert completed."
Write-Host "The Phase 143 test is intentionally checked separately."
Write-Host "If it still fails only because a Reference section precedes pi15^8,"
Write-Host "that confirms the regression predates/is independent of the frontier experiment."
Write-Host "Repository-wide tests were intentionally not run."
Write-Host "=============================================================="

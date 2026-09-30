$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-5E-2"
Write-Host "SHORT_EXACT_DERIVATION typed reason prose"
Write-Host "=============================================================="

$repoRoot = (Get-Location).Path
$testsPath = Join-Path $repoRoot "tests"
$env:PYTHONPATH = "$repoRoot;$testsPath"
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Applying minimal production change..."
  python `
    ".\phase150_rc4_5e_2_short_exact_derivation_reason\apply_phase150_rc4_5e_2.py"

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\toda_group_proof_generic_narrative_renderer.py" `
    ".\toda_group_proof_narrative_argument_body_renderer.py" `
    ".\tests\test_phase150_rc4_5e_2_short_exact_derivation_reason.py"

  Write-Host ""
  Write-Host "C. RC4-5E-2 focused tests..."
  python -m pytest -q `
    ".\tests\test_phase150_rc4_5e_2_short_exact_derivation_reason.py" `
    ".\tests\test_phase143_2_generic_short_exact_sequence.py" `
    ".\tests\test_phase143_42_argument_body_contribution_renderer.py" `
    ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py" `
    ".\tests\test_phase150_rc4_5d_3_multiple_relation_to_order.py" `
    ".\tests\test_phase149_rc3_4_cross_group_ordering.py"

  Write-Host ""
  Write-Host "D. Visible pi_6^3 Narrative check..."
  python `
    ".\phase150_rc4_5e_2_short_exact_derivation_reason\show_phase150_rc4_5e_2.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC4-5E-2 focused implementation completed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}

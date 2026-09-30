$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-5B-3 Minimal typed implementation"
Write-Host "Reference application + variable binding"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Applying minimal typed implementation..."
  python `
    ".\phase150_rc4_5b_3_minimal_typed_implementation\apply_phase150_rc4_5b_3.py"

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\toda_group_proof_narrative_semantics.py" `
    ".\toda_group_proof_narrative_reasons.py" `
    ".\toda_group_proof_narrative_reason_renderer.py" `
    ".\tests\test_phase150_rc4_5b_3_reference_binding.py"

  Write-Host ""
  Write-Host "C. RC4-5B-3 focused tests..."
  python -m pytest -q `
    ".\tests\test_phase150_rc4_4_reasons.py" `
    ".\tests\test_phase150_rc4_5_visible_reasons.py" `
    ".\tests\test_phase150_rc4_5b_3_reference_binding.py"

  Write-Host ""
  Write-Host "D. Visible typed-reference audit..."
  python `
    ".\phase150_rc4_5b_3_minimal_typed_implementation\audit_phase150_rc4_5b_3.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC4-5B-3 completed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "Next: Web Narrative visual confirmation."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}

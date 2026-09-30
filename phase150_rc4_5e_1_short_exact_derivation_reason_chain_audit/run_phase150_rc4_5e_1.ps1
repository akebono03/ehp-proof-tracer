$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-5E-1"
Write-Host "SHORT_EXACT_DERIVATION reason-chain audit"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$repoRoot = (Get-Location).Path
$testsPath = Join-Path $repoRoot "tests"
$env:PYTHONPATH = "$repoRoot;$testsPath"
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Syntax preflight..."
  python -m py_compile `
    ".\phase150_rc4_5e_1_short_exact_derivation_reason_chain_audit\audit_phase150_rc4_5e_1.py"

  Write-Host ""
  Write-Host "B. Typed reason-chain audit..."
  python `
    ".\phase150_rc4_5e_1_short_exact_derivation_reason_chain_audit\audit_phase150_rc4_5e_1.py"

  Write-Host ""
  Write-Host "C. Related focused regression..."
  python -m pytest -q `
    ".\tests\test_phase143_2_generic_short_exact_sequence.py" `
    ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py" `
    ".\tests\test_phase149_rc3_4_cross_group_ordering.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC4-5E-1 audit completed."
  Write-Host "Production changes: none"
  Write-Host "Existing test changes: none"
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}

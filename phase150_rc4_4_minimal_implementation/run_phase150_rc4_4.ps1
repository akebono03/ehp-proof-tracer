$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-4 Minimal implementation"
Write-Host "Typed generic reason infrastructure"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Applying minimal production implementation..."
  python `
    ".\phase150_rc4_4_minimal_implementation\apply_phase150_rc4_4.py"

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\toda_group_proof_narrative_reasons.py" `
    ".\tests\test_phase150_rc4_4_reasons.py"

  Write-Host ""
  Write-Host "C. RC4-4 focused tests..."
  python -m pytest -q `
    ".\tests\test_phase150_rc4_4_reasons.py" `
    ".\tests\test_phase143_19_method_evidence.py" `
    ".\tests\test_phase149_rc3_3_minimal_ordering.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 150 / RC4-4 minimal implementation completed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "Next: RC4-5 Cross-group audit."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}

$ErrorActionPreference = "Stop"
Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-5 Cross-group audit + visible Narrative integration"
Write-Host "=============================================================="
$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"
try {
  Write-Host ""
  Write-Host "A. Applying visible reason integration..."
  python ".\phase150_rc4_5_visible_reason_integration\apply_phase150_rc4_5.py"
  Write-Host ""
  Write-Host "B. Syntax preflight..."
  python -m py_compile ".\toda_group_proof_narrative_reason_renderer.py" ".\toda_group_proof_narrative_contribution_renderer.py" ".\tests\test_phase150_rc4_5_visible_reasons.py"
  Write-Host ""
  Write-Host "C. RC4-5 focused tests..."
  python -m pytest -q ".\tests\test_phase150_rc4_4_reasons.py" ".\tests\test_phase150_rc4_5_visible_reasons.py" ".\tests\test_phase149_rc3_3_minimal_ordering.py" ".\tests\test_phase134_9_pi6_3_snapshot.py"
  Write-Host ""
  Write-Host "D. Six-group visible reason audit..."
  python ".\phase150_rc4_5_visible_reason_integration\audit_phase150_rc4_5.py"
  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 150 / RC4-5 completed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "Restart the Web app and inspect pi_6^3 Narrative."
  Write-Host "Expected new sentence:"
  Write-Host "  この前提条件を満たすので、次の定義を用いる."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}

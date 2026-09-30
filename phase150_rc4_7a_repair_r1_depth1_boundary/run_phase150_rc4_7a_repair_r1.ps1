$ErrorActionPreference = "Stop"
Write-Host "=============================================================="
Write-Host "Phase 150 RC4-7A Repair R1"
Write-Host "Restore the depth=1 legacy Narrative boundary"
Write-Host "=============================================================="
$repoRoot = (Get-Location).Path
$env:PYTHONPATH = $repoRoot
$env:PYTHONIOENCODING = "utf-8"
try {
  Write-Host ""
  Write-Host "A. Applying minimal boundary repair..."
  python ".\phase150_rc4_7a_repair_r1_depth1_boundary\apply_phase150_rc4_7a_repair_r1.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  python -m py_compile ".\toda_group_proof_narrative_renderer.py" ".\tests\test_phase150_rc4_7a_cross_group_reference_normalization.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "C. RC4-7A tests including depth=1 boundary..."
  python -m pytest -q ".\tests\test_phase150_rc4_7a_cross_group_reference_normalization.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "D. Phase 134 pi15_8 Narrative regression..."
  python -m pytest -q ".\tests\test_phase134_24_pi15_8_narrative.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "E. Existing focused RC4 / six-group regression..."
  python -m pytest -q ".\tests\test_phase144_6_r25_20_six_group_generic_production_narrative.py" ".\tests\test_phase150_rc4_closure_reason_visibility.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "F. Visible depth=2 Narrative samples..."
  python -c "from tests.test_phase150_rc4_7a_cross_group_reference_normalization import _render_group; [print('='*78, '\npi_%s^%s\n'%(n+k,n), _render_group(n,k)) for n,k in ((4,6),(5,7),(9,7))]"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC4-7A Repair R1 completed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "Next boundary after inspection: RC4-7B argument-flow repair."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}

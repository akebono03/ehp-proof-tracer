$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 RC4-7B Production Repair R1"
Write-Host "Generic TARGET-support conclusion connector"
Write-Host "=============================================================="
Write-Host ""

$RepoRoot = (Get-Location).Path
$PackageDir = Join-Path $RepoRoot "phase150_rc4_7b_production_repair_r1"

$env:PYTHONPATH = $RepoRoot
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host "A. Applying minimal production repair..."
  python (Join-Path $PackageDir "apply_phase150_rc4_7b_production_repair_r1.py")
  if ($LASTEXITCODE -ne 0) {
    throw "Production repair failed."
  }

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\toda_group_proof_narrative_transition_renderer.py" `
    ".\tests\test_phase150_rc4_7b_production_repair.py"
  if ($LASTEXITCODE -ne 0) {
    throw "Syntax preflight failed."
  }

  Write-Host ""
  Write-Host "C. RC4-7B focused tests..."
  python -m pytest -q `
    tests/test_phase150_rc4_7b_production_repair.py
  if ($LASTEXITCODE -ne 0) {
    throw "RC4-7B focused tests failed."
  }

  Write-Host ""
  Write-Host "D. Related Narrative regression tests..."
  python -m pytest -q `
    tests/test_phase143_41_argument_local_body.py `
    tests/test_phase143_46_multi_argument_narrative_assembler.py `
    tests/test_phase143_53a_narrative_transitions.py `
    tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py `
    tests/test_phase147_rc1_argument_method_ownership.py `
    tests/test_phase148_rc2_4_repair_r5.py `
    tests/test_phase148_rc2_4_repair_r5_r2.py `
    tests/test_phase150_rc4_7a_cross_group_reference_normalization.py
  if ($LASTEXITCODE -ne 0) {
    throw "Related Narrative regression tests failed."
  }

  Write-Host ""
  Write-Host "E. Visible Narrative snapshots..."
  python (Join-Path $PackageDir "show_phase150_rc4_7b_narratives.py")
  if ($LASTEXITCODE -ne 0) {
    throw "Narrative snapshot failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC4-7B Production Repair R1 completed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}

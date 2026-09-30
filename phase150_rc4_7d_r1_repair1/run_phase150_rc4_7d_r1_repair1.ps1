$ErrorActionPreference = "Stop"
Write-Host "=============================================================="
Write-Host "Phase 150 RC4-7D R1 Repair 1"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$PackageDir = Join-Path $RepoRoot "phase150_rc4_7d_r1_repair1"
$env:PYTHONPATH = $RepoRoot
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host "A. Applying minimal repair..."
  python (Join-Path $PackageDir "apply_phase150_rc4_7d_r1_repair1.py")
  if ($LASTEXITCODE -ne 0) { throw "repair apply failed" }

  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\toda_group_proof_narrative_reason_renderer.py" `
    ".\tests\test_phase150_rc4_7d_reason_hidden_conclusion_anchor.py"
  if ($LASTEXITCODE -ne 0) { throw "syntax preflight failed" }

  Write-Host "C. RC4-7D focused tests..."
  python -m pytest -q `
    tests/test_phase150_rc4_7d_generic_reason_vocabulary.py `
    tests/test_phase150_rc4_7d_reason_hidden_conclusion_anchor.py
  if ($LASTEXITCODE -ne 0) { throw "RC4-7D focused tests failed" }

  Write-Host "D. Related Narrative regression tests..."
  $Tests = @(
    "tests/test_phase143_46_multi_argument_narrative_assembler.py",
    "tests/test_phase143_53a_narrative_transitions.py",
    "tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py",
    "tests/test_phase150_rc4_7a_cross_group_reference_normalization.py"
  ) | Where-Object { Test-Path $_ }
  if ($Tests.Count -gt 0) {
    python -m pytest -q $Tests
    if ($LASTEXITCODE -ne 0) { throw "related regression tests failed" }
  }

  Write-Host "E. Visible Narrative snapshots..."
  python (Join-Path $PackageDir "show_phase150_rc4_7d_repair1_narratives.py")
  if ($LASTEXITCODE -ne 0) { throw "snapshot failed" }

  Write-Host "=============================================================="
  Write-Host "RC4-7D R1 Repair 1 completed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}

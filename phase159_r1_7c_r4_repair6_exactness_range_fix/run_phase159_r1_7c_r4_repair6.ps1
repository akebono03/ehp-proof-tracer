$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 R1-7c R4 repair6 - exactness range fix"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

$OriginalPythonPath = $env:PYTHONPATH

if ([string]::IsNullOrWhiteSpace($OriginalPythonPath)) {
  $env:PYTHONPATH = $RepoRoot
}
else {
  $env:PYTHONPATH = $RepoRoot + [IO.Path]::PathSeparator + $OriginalPythonPath
}

try {
  Write-Host "[1/6] Apply repair6"

  python ".\phase159_r1_7c_r4_repair6_exactness_range_fix\apply_phase159_r1_7c_r4_repair6.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Repair6 apply failed with exit code $LASTEXITCODE."
  }

  Write-Host ""
  Write-Host "[2/6] Syntax-check production modules"

  python -m py_compile `
    ".\toda_group_proof_narrative_reason_renderer.py" `
    ".\toda_group_proof_generic_narrative_renderer.py" `
    ".\toda_group_proof_narrative_renderer.py" `
    ".\toda_group_proof_narrative_contribution_renderer.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Syntax check failed with exit code $LASTEXITCODE."
  }

  Write-Host ""
  Write-Host "[3/6] Run Phase150 focused regressions"

  python -m pytest `
    "tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py" `
    "tests/test_phase150_rc4_5f_2_final_group_structure_reason.py" `
    -q `
    --tb=short

  if ($LASTEXITCODE -ne 0) {
    throw "Phase150 regressions failed with exit code $LASTEXITCODE."
  }

  Write-Host ""
  Write-Host "[4/6] Run Phase157 focused regressions"

  python -m pytest `
    "tests/test_phase157_r11_reference_reason_punctuation.py" `
    "tests/test_phase157_r20_repair16_proof_order_and_cleanup.py" `
    "tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py" `
    -q `
    --tb=short

  if ($LASTEXITCODE -ne 0) {
    throw "Phase157 regressions failed with exit code $LASTEXITCODE."
  }

  Write-Host ""
  Write-Host "[5/6] Run Phase159 R4 repair6 focused regression"

  python -m pytest `
    "tests/test_phase159_r1_7c_r4_repair6_residual_proof_prose_normalization.py" `
    -q `
    --tb=short

  if ($LASTEXITCODE -ne 0) {
    throw "Phase159 repair6 regression failed with exit code $LASTEXITCODE."
  }

  Write-Host ""
  Write-Host "[6/6] Re-run R4 cross-group audit"

  python ".\phase159_r1_7c_r4_cross_group_structural_audit\audit_phase159_r1_7c_r4.py"

  if ($LASTEXITCODE -ne 0) {
    throw "R4 re-audit failed with exit code $LASTEXITCODE."
  }

  Write-Host ""
  Get-Content `
    ".\phase159_r1_7c_r4_cross_group_structural_audit\output\summary.md" `
    -Encoding UTF8

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 159 R1-7c R4 repair6 verification complete"
  Write-Host "Repository-wide pytest: NOT RUN"
  Write-Host "=============================================================="
}
finally {
  $env:PYTHONPATH = $OriginalPythonPath
}

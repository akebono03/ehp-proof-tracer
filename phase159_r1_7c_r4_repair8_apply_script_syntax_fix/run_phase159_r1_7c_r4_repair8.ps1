
$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot
Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 R1-7c R4 repair8 - apply-script syntax fix"
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
  Write-Host "[1/8] Syntax-check repair8 apply script"
  python -m py_compile `
    ".\phase159_r1_7c_r4_repair8_apply_script_syntax_fix\apply_phase159_r1_7c_r4_repair8.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Repair8 apply-script syntax check failed with exit code $LASTEXITCODE."
  }

  Write-Host ""
  Write-Host "[2/8] Apply repair8"
  python ".\phase159_r1_7c_r4_repair8_apply_script_syntax_fix\apply_phase159_r1_7c_r4_repair8.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Repair8 apply failed with exit code $LASTEXITCODE."
  }

  Write-Host ""
  Write-Host "[3/8] Syntax-check production modules"
  python -m py_compile `
    ".\toda_group_proof_narrative_reason_renderer.py" `
    ".\toda_group_proof_generic_narrative_renderer.py" `
    ".\toda_group_proof_narrative_renderer.py" `
    ".\toda_group_proof_narrative_contribution_renderer.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Production syntax check failed with exit code $LASTEXITCODE."
  }

  Write-Host ""
  Write-Host "[4/8] Run Phase150 focused regressions"
  python -m pytest `
    "tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py" `
    "tests/test_phase150_rc4_5f_2_final_group_structure_reason.py" `
    -q `
    --tb=short

  if ($LASTEXITCODE -ne 0) {
    throw "Phase150 regressions failed with exit code $LASTEXITCODE."
  }

  Write-Host ""
  Write-Host "[5/8] Run affected Phase157 prose regressions"
  python -m pytest `
    "tests/test_phase157_r11_r17_residual_narrative_defects.py" `
    "tests/test_phase157_r20_repair43_dangling_connector_cleanup.py" `
    "tests/test_phase157_r20_repair18_eta_bridge_consumer_anchor.py" `
    "tests/test_phase157_r20_repair32_exactness_intro_anchor.py" `
    "tests/test_phase157_r20_repair16_proof_order_and_cleanup.py" `
    "tests/test_phase157_r19_pi6_3_reference_dependency_restoration.py" `
    -q `
    --tb=short

  if ($LASTEXITCODE -ne 0) {
    throw "Phase157 prose regressions failed with exit code $LASTEXITCODE."
  }

  Write-Host ""
  Write-Host "[6/8] Run repair6 regression"
  python -m pytest `
    "tests/test_phase159_r1_7c_r4_repair6_residual_proof_prose_normalization.py" `
    -q `
    --tb=short

  if ($LASTEXITCODE -ne 0) {
    throw "Repair6 regression failed with exit code $LASTEXITCODE."
  }

  Write-Host ""
  Write-Host "[7/8] Run repair8 focused regression"
  python -m pytest `
    "tests/test_phase159_r1_7c_r4_repair8_final_group_reason_and_stale_expectations.py" `
    -q `
    --tb=short

  if ($LASTEXITCODE -ne 0) {
    throw "Repair8 focused regression failed with exit code $LASTEXITCODE."
  }

  Write-Host ""
  Write-Host "[8/8] Re-run R4 cross-group audit"
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
  Write-Host "Phase 159 R1-7c R4 repair8 verification complete"
  Write-Host "Repository-wide pytest: NOT RUN"
  Write-Host "=============================================================="
}
finally {
  $env:PYTHONPATH = $OriginalPythonPath
}

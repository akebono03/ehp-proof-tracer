$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 R1-7c R4 repair1 - residual proof-prose normalization"
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
  Write-Host "[1/4] Apply R4 repair1"
  python ".\phase159_r1_7c_r4_repair1_residual_proof_prose_normalization\apply_phase159_r1_7c_r4_repair1.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase159 R1-7c R4 repair1 apply failed with exit code $LASTEXITCODE."
  }

  Write-Host ""
  Write-Host "[2/4] Run direct renderer regressions"
  python -m pytest `
    "tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py" `
    "tests/test_phase150_rc4_5f_2_final_group_structure_reason.py" `
    -q `
    --tb=short

  if ($LASTEXITCODE -ne 0) {
    throw "Direct renderer regressions failed with exit code $LASTEXITCODE."
  }

  Write-Host ""
  Write-Host "[3/4] Run Phase157 public Narrative regression"
  python -m pytest `
    "tests/test_phase157_r11_reference_reason_punctuation.py" `
    -q `
    --tb=short

  if ($LASTEXITCODE -ne 0) {
    throw "Phase157 public Narrative regression failed with exit code $LASTEXITCODE."
  }

  Write-Host ""
  Write-Host "[4/4] Run Phase159 R4 repair1 focused regression"
  python -m pytest `
    "tests/test_phase159_r1_7c_r4_repair1_residual_proof_prose_normalization.py" `
    -q `
    --tb=short

  if ($LASTEXITCODE -ne 0) {
    throw "Phase159 R4 repair1 focused regression failed with exit code $LASTEXITCODE."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 159 R1-7c R4 repair1 verification complete"
  Write-Host "Repository-wide pytest: NOT RUN"
  Write-Host "=============================================================="
}
finally {
  $env:PYTHONPATH = $OriginalPythonPath
}

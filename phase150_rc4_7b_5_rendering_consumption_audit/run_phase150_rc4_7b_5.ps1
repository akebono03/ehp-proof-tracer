$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 RC4-7B-5 Rendering Consumption Audit"
Write-Host "Production changes: none"
Write-Host "=============================================================="
Write-Host ""

$RepoRoot = (Get-Location).Path
$AuditDir = Join-Path $RepoRoot "phase150_rc4_7b_5_rendering_consumption_audit"
$AuditScript = Join-Path $AuditDir "audit_phase150_rc4_7b_5.py"
$OutputFile = Join-Path $AuditDir "rc4_7b_5_output.txt"

$env:PYTHONPATH = $RepoRoot
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host "A. Syntax preflight..."
  python -m py_compile $AuditScript
  if ($LASTEXITCODE -ne 0) {
    throw "Syntax preflight failed."
  }

  Write-Host ""
  Write-Host "B. Running rendering-consumption audit..."
  $AuditOutput = & python $AuditScript 2>&1
  $AuditExitCode = $LASTEXITCODE
  $AuditOutput | Tee-Object -FilePath $OutputFile
  if ($AuditExitCode -ne 0) {
    throw "RC4-7B-5 audit failed with exit code $AuditExitCode."
  }

  Write-Host ""
  Write-Host "C. Focused regression guard..."
  python -m pytest -q `
    tests/test_phase143_41_argument_local_body.py `
    tests/test_phase143_46_multi_argument_narrative_assembler.py `
    tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py `
    tests/test_phase147_rc1_argument_method_ownership.py `
    tests/test_phase148_rc2_4_repair_r5.py `
    tests/test_phase148_rc2_4_repair_r5_r2.py `
    tests/test_phase150_rc4_7a_cross_group_reference_normalization.py
  if ($LASTEXITCODE -ne 0) {
    throw "Focused regression guard failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC4-7B-5 audit completed."
  Write-Host "No production files or existing tests were changed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "Output: $OutputFile"
  Write-Host "Next: choose the minimal RC4-7B production repair from consumption classification."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}

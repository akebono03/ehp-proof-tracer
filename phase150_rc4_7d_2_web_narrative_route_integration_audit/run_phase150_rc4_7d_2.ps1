$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 RC4-7D-2 Web Narrative Route Integration Audit"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$AuditDir = Join-Path $RepoRoot "phase150_rc4_7d_2_web_narrative_route_integration_audit"
$OutputFile = Join-Path $AuditDir "rc4_7d_2_output.txt"

$env:PYTHONPATH = $RepoRoot
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host "A. Syntax preflight..."
  python -m py_compile `
    (Join-Path $AuditDir "audit_phase150_rc4_7d_2.py")
  if ($LASTEXITCODE -ne 0) {
    throw "syntax preflight failed"
  }

  Write-Host "B. Focused Web/Narrative regression guard..."
  $Tests = @(
    "tests/test_phase135_1_web_narrative_display_math.py",
    "tests/test_phase135_3_web_narrative_readability.py",
    "tests/test_phase143_46_multi_argument_narrative_assembler.py",
    "tests/test_phase150_rc4_7d_generic_reason_vocabulary.py",
    "tests/test_phase150_rc4_7d_reason_hidden_conclusion_anchor.py"
  ) | Where-Object { Test-Path $_ }

  if ($Tests.Count -gt 0) {
    python -m pytest -q $Tests
    if ($LASTEXITCODE -ne 0) {
      throw "focused regression guard failed"
    }
  }

  Write-Host "C. Route integration audit..."
  $AuditOutput = & python `
    (Join-Path $AuditDir "audit_phase150_rc4_7d_2.py") `
    2>&1
  $AuditExitCode = $LASTEXITCODE
  $AuditOutput | Tee-Object -FilePath $OutputFile
  if ($AuditExitCode -ne 0) {
    throw "route integration audit failed"
  }

  Write-Host "=============================================================="
  Write-Host "RC4-7D-2 audit completed."
  Write-Host "No production files, tests, or docs were changed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "Output: $OutputFile"
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}

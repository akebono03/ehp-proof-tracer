$ErrorActionPreference = "Stop"

$AuditDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $AuditDir
$AuditScript = Join-Path $AuditDir "audit_worktree_creation_failure.ps1"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-11-R6-R1-R2-R1-R2-R2-R2"
Write-Host "Worktree Creation Failure Diagnostic Audit"
Write-Host "Production changes: none"
Write-Host "Historical locator changes: none"
Write-Host "Population cache changes: none"
Write-Host "=============================================================="

Push-Location $RepoRoot

try {
  Write-Host ""
  Write-Host "A. PowerShell parser preflight..."
  $parseErrors = $null
  $parseTokens = $null

  [void][System.Management.Automation.Language.Parser]::ParseFile(
    $AuditScript,
    [ref]$parseTokens,
    [ref]$parseErrors
  )

  if ($parseErrors.Count -ne 0) {
    foreach ($parseError in $parseErrors) {
      Write-Host $parseError.Message
    }

    throw "Diagnostic audit parser preflight failed."
  }

  Write-Host "Diagnostic audit PowerShell parser preflight: PASS"

  Write-Host ""
  Write-Host "B. Focused audit-harness tests..."
  pytest -q `
    ".\phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r2_worktree_creation_failure_diagnostic_audit\test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r2.py"

  $testExitCode = $LASTEXITCODE

  if ($testExitCode -ne 0) {
    throw "Focused diagnostic audit tests failed with exit code $testExitCode"
  }

  Write-Host ""
  Write-Host "C. Running worktree creation diagnostic..."

  & powershell `
    -NoProfile `
    -NonInteractive `
    -ExecutionPolicy Bypass `
    -File $AuditScript `
    -RepoRoot $RepoRoot

  $auditExitCode = $LASTEXITCODE

  if ($auditExitCode -ne 0) {
    throw "Worktree diagnostic audit stopped with exit code $auditExitCode"
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-11-R6-R1-R2-R1-R2-R2-R2 diagnostic audit completed."
  Write-Host "No production files were modified."
  Write-Host "No historical locator files were modified."
  Write-Host "No population cache was modified."
  Write-Host "No full pytest was run."
  Write-Host "=============================================================="
}
finally {
  Pop-Location
}

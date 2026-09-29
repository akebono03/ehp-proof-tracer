$ErrorActionPreference = "Stop"

$RepairDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $RepairDir
$DiagnosticDir = Join-Path $RepoRoot "phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r2_worktree_creation_failure_diagnostic_audit"
$AuditScript = Join-Path $DiagnosticDir "audit_worktree_creation_failure.ps1"
$AuditTest = Join-Path $DiagnosticDir "test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r2.py"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-11-R6-R1-R2-R1-R2-R2-R2-R1"
Write-Host "Diagnostic Audit Test Repair"
Write-Host "Production changes: none"
Write-Host "Diagnostic PowerShell changes: none"
Write-Host "Historical locator changes: none"
Write-Host "Population cache changes: none"
Write-Host "=============================================================="

Push-Location $RepoRoot

try {
  Write-Host ""
  Write-Host "A. Applying audit-test-only repair..."

  python ".\phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r2_r1_diagnostic_audit_test_repair\apply_r25_11_r6_r1_r2_r1_r2_r2_r2_r1.py"

  $applyExitCode = $LASTEXITCODE

  if ($applyExitCode -ne 0) {
    throw "Diagnostic audit test repair failed with exit code $applyExitCode"
  }

  Write-Host ""
  Write-Host "B. Confirming diagnostic PowerShell still parses..."
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
  Write-Host "C. Focused diagnostic audit tests..."

  pytest -q $AuditTest

  $testExitCode = $LASTEXITCODE

  if ($testExitCode -ne 0) {
    throw "Focused diagnostic audit tests failed with exit code $testExitCode"
  }

  Write-Host ""
  Write-Host "D. Running worktree creation diagnostic..."

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
  Write-Host "R25-11-R6-R1-R2-R1-R2-R2-R2-R1 completed."
  Write-Host "No production files were modified."
  Write-Host "No diagnostic PowerShell was modified."
  Write-Host "No historical locator was modified."
  Write-Host "No population cache was modified."
  Write-Host "No full pytest was run."
  Write-Host "=============================================================="
}
finally {
  Pop-Location
}

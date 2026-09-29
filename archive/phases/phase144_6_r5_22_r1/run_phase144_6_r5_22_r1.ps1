$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "Phase 144-6-R5-22-R1 runner repair."
Write-Host "Production/audit/test source changes: none."
Write-Host "Repair: add repo tests directory to PYTHONPATH for standalone audit."

Push-Location $RepoRoot
try {
  $RepoPath = (Get-Location).Path
  $TestsPath = Join-Path $RepoPath "tests"
  $env:PYTHONPATH = "$RepoPath;$TestsPath"

  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R5-22 targeted tests"
  Write-Host ("=" * 78)

  pytest -q `
    ".\tests\test_phase144_6_r5_21_missing_7_facts_generic_provider_audit.py" `
    ".\tests\test_phase144_6_r5_22_missing_4_facts_statement_structure_audit.py"

  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R5-22 statement-structure audit"
  Write-Host ("=" * 78)

  python ".\audit_phase144_6_r5_22.py"

  exit $LASTEXITCODE
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}

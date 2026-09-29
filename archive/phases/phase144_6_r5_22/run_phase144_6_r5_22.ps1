$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Copy-Item `
  -Path (Join-Path $PackageDir "payload\audit_phase144_6_r5_22.py") `
  -Destination (Join-Path $RepoRoot "audit_phase144_6_r5_22.py") `
  -Force

Copy-Item `
  -Path (Join-Path $PackageDir "payload\tests\test_phase144_6_r5_22_missing_4_facts_statement_structure_audit.py") `
  -Destination (Join-Path $RepoRoot "tests\test_phase144_6_r5_22_missing_4_facts_statement_structure_audit.py") `
  -Force

Write-Host "Phase 144-6-R5-22 audit files applied."
Write-Host "Added/replaced only:"
Write-Host "  audit_phase144_6_r5_22.py"
Write-Host "  tests/test_phase144_6_r5_22_missing_4_facts_statement_structure_audit.py"

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path

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

$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Copy-Item `
  -Path (Join-Path $PackageDir "payload\audit_phase144_6_r5_31.py") `
  -Destination (Join-Path $RepoRoot "audit_phase144_6_r5_31.py") `
  -Force

Copy-Item `
  -Path (Join-Path $PackageDir "payload\tests\test_phase144_6_r5_31_upstream_calculation_attachment_semantic_audit.py") `
  -Destination (Join-Path $RepoRoot "tests\test_phase144_6_r5_31_upstream_calculation_attachment_semantic_audit.py") `
  -Force

Write-Host "Phase 144-6-R5-31 audit files applied."
Write-Host "Added/replaced only:"
Write-Host "  audit_phase144_6_r5_31.py"
Write-Host "  tests/test_phase144_6_r5_31_upstream_calculation_attachment_semantic_audit.py"
Write-Host "Production code changes: none."

Push-Location $RepoRoot
try {
  $RepoPath = (Get-Location).Path
  $TestsPath = Join-Path $RepoPath "tests"
  $env:PYTHONPATH = "$RepoPath;$TestsPath"

  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R5-31 targeted tests"
  Write-Host ("=" * 78)

  pytest -q `
    ".\tests\test_phase144_6_r5_30_upstream_calculation_attachment_audit.py" `
    ".\tests\test_phase144_6_r5_31_upstream_calculation_attachment_semantic_audit.py"

  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R5-31 audit"
  Write-Host ("=" * 78)

  python ".\audit_phase144_6_r5_31.py"
  exit $LASTEXITCODE
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}

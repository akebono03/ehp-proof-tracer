$ErrorActionPreference = "Stop"
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $PackageDir "..")

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path

  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R3 reference mapping audit"
  Write-Host "AUDIT ONLY - no production source changes"
  Write-Host ("=" * 78)

  python ".\phase144_6_r3_reference_mapping_audit\audit_phase144_6_r3_references.py"
  if ($LASTEXITCODE -ne 0) { throw "Phase 144-6-R3 audit failed." }

  Write-Host ""
  Write-Host ("=" * 78)
  Write-Host "Focused regression only (NOT full pytest)"
  Write-Host ("=" * 78)

  pytest -q `
    ".\tests\test_phase144_6_pi6_generic_production_route.py" `
    ".\tests\test_phase143_49_dependency_label_narrative_policy.py"

  if ($LASTEXITCODE -ne 0) { throw "Focused regression failed." }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}

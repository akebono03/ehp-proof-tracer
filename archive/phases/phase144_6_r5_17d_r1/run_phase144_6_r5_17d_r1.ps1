$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Copy-Item `
  -Path (Join-Path $PackageDir "payload\audit_phase144_6_r5_17d_r1.py") `
  -Destination (Join-Path $RepoRoot "audit_phase144_6_r5_17d_r1.py") `
  -Force

Copy-Item `
  -Path (Join-Path $PackageDir "payload\tests\test_phase144_6_r5_17d_r1_other_semantic_role_resolution.py") `
  -Destination (Join-Path $RepoRoot "tests\test_phase144_6_r5_17d_r1_other_semantic_role_resolution.py") `
  -Force

Write-Host "Phase 144-6-R5-17D-R1 audit files applied."
Write-Host "Added/replaced only:"
Write-Host "  audit_phase144_6_r5_17d_r1.py"
Write-Host "  tests/test_phase144_6_r5_17d_r1_other_semantic_role_resolution.py"

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path
  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R5-17D-R1 targeted tests"
  Write-Host ("=" * 78)
  pytest -q ".\tests\test_phase144_6_r5_17d_r1_other_semantic_role_resolution.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R5-17D-R1 audit"
  Write-Host ("=" * 78)
  python ".\audit_phase144_6_r5_17d_r1.py"
  exit $LASTEXITCODE
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}

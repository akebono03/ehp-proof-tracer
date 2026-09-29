$ErrorActionPreference = "Stop"
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $PackageDir "..")

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path

  Write-Host ("=" * 78)
  Write-Host "Phase 144-6: pi_6^3 generic-only production route"
  Write-Host ("=" * 78)

  python ".\phase144_6_pi6_generic_production_route\apply_phase144_6.py"
  if ($LASTEXITCODE -ne 0) { throw "Phase 144-6 patch failed." }

  python ".\phase144_6_pi6_generic_production_route\install_phase144_6_test.py"
  if ($LASTEXITCODE -ne 0) { throw "Phase 144-6 test install failed." }

  Write-Host ""
  Write-Host ("=" * 78)
  Write-Host "Focused tests only (NOT full pytest)"
  Write-Host ("=" * 78)

  pytest -q `
    ".\tests\test_phase144_6_pi6_generic_production_route.py" `
    ".\tests\test_phase143_49_dependency_label_narrative_policy.py" `
    ".\tests\test_phase143_2_generic_short_exact_sequence.py" `
    ".\tests\test_phase142_3_generic_proof_text.py"

  if ($LASTEXITCODE -ne 0) { throw "Phase 144-6 focused tests failed." }

  Write-Host ""
  Write-Host ("=" * 78)
  Write-Host "CLI production preview"
  Write-Host ("=" * 78)

  python ".\main.py" group-proof 3 3 --depth 2 --mode narrative
  if ($LASTEXITCODE -ne 0) { throw "Phase 144-6 CLI preview failed." }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}

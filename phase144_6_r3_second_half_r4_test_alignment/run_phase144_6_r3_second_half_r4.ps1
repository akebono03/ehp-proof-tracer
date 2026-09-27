$ErrorActionPreference = "Stop"
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $PackageDir "..")

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path

  python ".\phase144_6_r3_second_half_r4_test_alignment\apply_phase144_6_r3_second_half_r4.py"
  if ($LASTEXITCODE -ne 0) { throw "R3 test alignment failed." }

  python -m py_compile `
    ".\tests\test_phase144_6_pi6_generic_production_route.py"
  if ($LASTEXITCODE -ne 0) { throw "py_compile failed." }

  pytest -q `
    ".\tests\test_phase144_6_r3_structured_references.py" `
    ".\tests\test_phase144_6_r3_production_references.py" `
    ".\tests\test_phase96_proof_step_source_presentation.py" `
    ".\tests\test_phase143_49_dependency_label_narrative_policy.py" `
    ".\tests\test_phase144_6_pi6_generic_production_route.py"
  if ($LASTEXITCODE -ne 0) { throw "Focused tests failed." }

  Write-Host ""
  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R3 final production preview"
  Write-Host ("=" * 78)
  python ".\phase144_6_r3_second_half_r4_test_alignment\preview_phase144_6_r3_completion.py"
  if ($LASTEXITCODE -ne 0) { throw "Preview failed." }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}

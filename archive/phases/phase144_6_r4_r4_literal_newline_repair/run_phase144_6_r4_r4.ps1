$ErrorActionPreference = "Stop"
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $PackageDir "..")

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path

  python ".\phase144_6_r4_r4_literal_newline_repair\apply_phase144_6_r4_r4.py"
  if ($LASTEXITCODE -ne 0) { throw "R4-R4 apply failed." }

  python -m py_compile `
    ".\toda_group_proof_narrative_argument_multi_renderer.py" `
    ".\tests\test_phase144_6_r4_supporting_fact_filtering.py"
  if ($LASTEXITCODE -ne 0) { throw "py_compile failed." }

  pytest -q `
    ".\tests\test_phase144_6_r4_supporting_fact_filtering.py" `
    ".\tests\test_phase144_6_r3_structured_references.py" `
    ".\tests\test_phase144_6_r3_production_references.py" `
    ".\tests\test_phase143_49_dependency_label_narrative_policy.py" `
    ".\tests\test_phase144_6_pi6_generic_production_route.py"
  if ($LASTEXITCODE -ne 0) { throw "Focused tests failed." }

  Write-Host ""
  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R4-R4 filtered Narrative preview"
  Write-Host ("=" * 78)
  python ".\phase144_6_r4_frontier_filter_impl\preview_phase144_6_r4.py"
  if ($LASTEXITCODE -ne 0) { throw "Preview failed." }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}

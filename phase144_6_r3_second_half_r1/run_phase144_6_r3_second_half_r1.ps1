$ErrorActionPreference = "Stop"
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $PackageDir "..")

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path

  python ".\phase144_6_r3_second_half_r1\repair_phase144_6_r3_second_half_r1.py"
  if ($LASTEXITCODE -ne 0) { throw "R3 second-half R1 repair failed." }

  python -m py_compile `
    ".\proof.py" `
    ".\toda_rules.py" `
    ".\toda_group_proof_narrative_references.py" `
    ".\toda_group_proof_narrative_argument_multi_renderer.py"
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
  Write-Host "Phase 144-6-R3 production reference preview"
  Write-Host ("=" * 78)
  python ".\phase144_6_r3_second_half\preview_phase144_6_r3.py"
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}

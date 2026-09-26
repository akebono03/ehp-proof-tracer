$ErrorActionPreference = "Stop"
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $PackageDir "..")

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path

  Copy-Item `
    ".\phase144_6_r3_r1_syntax_repair\toda_group_proof_narrative_references.py" `
    ".\toda_group_proof_narrative_references.py" `
    -Force

  Write-Host "Phase 144-6-R3-R1 syntax repair applied."
  Write-Host "Replaced only: toda_group_proof_narrative_references.py"

  python -m py_compile ".\toda_group_proof_narrative_references.py"
  if ($LASTEXITCODE -ne 0) { throw "py_compile failed." }

  pytest -q `
    ".\tests\test_phase144_6_r3_structured_references.py" `
    ".\tests\test_phase96_proof_step_source_presentation.py" `
    ".\tests\test_phase144_6_pi6_generic_production_route.py"

  if ($LASTEXITCODE -ne 0) { throw "Focused tests failed." }

  python -c "from proof import InferenceRule; import inspect; print(inspect.signature(InferenceRule))"
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}

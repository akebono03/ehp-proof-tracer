$ErrorActionPreference = "Stop"
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $PackageDir "..")

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path

  python ".\phase144_6_r3_impl\apply_phase144_6_r3.py"
  if ($LASTEXITCODE -ne 0) { throw "R3 apply failed." }

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

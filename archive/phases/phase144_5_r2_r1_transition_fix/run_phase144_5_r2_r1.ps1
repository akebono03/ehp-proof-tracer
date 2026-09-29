$ErrorActionPreference="Stop"
$PackageDir=Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot=Resolve-Path (Join-Path $PackageDir "..")
Push-Location $RepoRoot
try {
  $env:PYTHONPATH=(Get-Location).Path
  python ".\phase144_5_r2_r1_transition_fix\apply_phase144_5_r2_r1.py"
  if ($LASTEXITCODE -ne 0) { throw "patch failed" }
  pytest -q `
    ".\tests\test_phase143_49_dependency_label_narrative_policy.py" `
    ".\tests\test_phase142_3_generic_proof_text.py" `
    ".\tests\test_phase143_2_generic_short_exact_sequence.py"
  if ($LASTEXITCODE -ne 0) { throw "focused regression failed" }
  python ".\phase144_5_generic_definition_order_equations\preview_phase144_5.py"
} finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}

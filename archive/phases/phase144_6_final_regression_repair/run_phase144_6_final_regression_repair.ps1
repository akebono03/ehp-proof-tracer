$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$TestsDir = Join-Path $RepoRoot "tests"
$OldPythonPath = $env:PYTHONPATH

try {
  $env:PYTHONPATH = "$RepoRoot;$TestsDir"

  pytest -q `
    ".\tests\test_phase133_7_group_proof_narrative_labels.py" `
    ".\tests\test_phase134_16_presentation_catalog.py" `
    ".\tests\test_phase134_3_pi6_3_numbered_narrative.py" `
    ".\tests\test_phase134_5_pi6_3_reference_fact_split.py" `
    ".\tests\test_phase134_6_pi6_3_mathbook_narrative.py" `
    ".\tests\test_phase134_7_pi6_3_final_narrative.py" `
    ".\tests\test_phase134_9_pi6_3_snapshot.py" `
    ".\tests\test_phase136_1_pi6_3_narrative_prose.py" `
    ".\tests\test_phase136_2_pi6_3_narrative_structure.py" `
    ".\tests\test_phase144_6_public_route_cutover.py" `
    ".\tests\test_phase144_6_r5_43_11d_final_completion_audit.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Phase 144-6 Final Regression Repair focused tests failed."
  }

  Write-Host ""
  Write-Host "Phase 144-6 Final Regression Repair focused tests: PASS"
  Write-Host "Full suite is intentionally NOT run in this package."
}
finally {
  if ($null -eq $OldPythonPath) {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  }
  else {
    $env:PYTHONPATH = $OldPythonPath
  }
}

$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$TestsDir = Join-Path $RepoRoot "tests"
$TestsInit = Join-Path $TestsDir "__init__.py"
$CreatedTestsInit = $false
$OldPythonPath = $env:PYTHONPATH
$Code = 1

Write-Host "=============================================================="
Write-Host "Phase 144-6 Final Regression Repair R2"
Write-Host "Focused runner dual-import repair"
Write-Host "Production code changes: none"
Write-Host "Test code changes in R2: none"
Write-Host "=============================================================="

if (-not (Test-Path $TestsDir)) {
  throw "tests directory was not found: $TestsDir"
}

if (-not (Test-Path $TestsInit)) {
  New-Item -ItemType File -Path $TestsInit -Force | Out-Null
  $CreatedTestsInit = $true
  Write-Host "Temporary package marker created: tests/__init__.py"
} else {
  Write-Host "Existing tests/__init__.py preserved."
}

$env:PYTHONPATH = "$RepoRoot;$TestsDir"

try {
  Write-Host ""
  Write-Host "Running dual-import preflight..."
  python -c "import tests.test_phase143_19_method_evidence; import test_phase143_19_method_evidence; print('Focused dual import preflight: PASS')"

  if ($LASTEXITCODE -ne 0) {
    throw "Focused dual import preflight failed."
  }

  Write-Host ""
  Write-Host "Running Phase 144-6 Final Regression Repair focused tests..."

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

  $Code = $LASTEXITCODE
}
finally {
  if ($null -eq $OldPythonPath) {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  } else {
    $env:PYTHONPATH = $OldPythonPath
  }

  if ($CreatedTestsInit -and (Test-Path $TestsInit)) {
    Remove-Item $TestsInit -Force
    Write-Host ""
    Write-Host "Temporary package marker removed: tests/__init__.py"
  }
}

if ($Code -ne 0) {
  Write-Host ""
  Write-Host "Phase 144-6 Final Regression Repair R2 focused tests: FAIL"
  exit $Code
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 144-6 Final Regression Repair R2 focused tests: PASS"
Write-Host "=============================================================="
Write-Host "Production code changes in R2: none."
Write-Host "Test code changes in R2: none."
Write-Host "Next step after PASS: rerun canonical Phase-end full suite R4."

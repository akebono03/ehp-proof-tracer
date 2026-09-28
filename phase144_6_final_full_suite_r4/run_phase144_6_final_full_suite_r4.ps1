$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$TestsDir = Join-Path $RepoRoot "tests"
$TestsInit = Join-Path $TestsDir "__init__.py"
$CreatedTestsInit = $false
$OldPythonPath = $env:PYTHONPATH

Write-Host "=============================================================="
Write-Host "Phase 144-6 Final Full Suite R4"
Write-Host "Dual test-import compatibility runner"
Write-Host "Production changes: none"
Write-Host "Persistent test changes: none"
Write-Host "=============================================================="

if (-not (Test-Path $TestsDir)) {
  throw "tests directory was not found: $TestsDir"
}

$RequiredHelpers = @(
  (Join-Path $TestsDir "test_phase143_19_method_evidence.py"),
  (Join-Path $TestsDir "test_phase105_14_qualified_execution_family_grouping.py"),
  (Join-Path $TestsDir "test_phase144_6_r5_18_production_generic_proof_chain_foundation.py")
)

foreach ($RequiredHelper in $RequiredHelpers) {
  if (-not (Test-Path $RequiredHelper)) {
    throw "Required canonical test helper was not found: $RequiredHelper"
  }
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
  Write-Host "PYTHONPATH configured for both import styles:"
  Write-Host "  package style:   from tests.test_phase... import ..."
  Write-Host "  top-level style: from test_phase... import ..."
  Write-Host ""

  Write-Host "Running import preflight..."
  python -c "import tests.test_phase143_19_method_evidence; import test_phase105_14_qualified_execution_family_grouping; import tests.test_phase144_6_r5_18_production_generic_proof_chain_foundation; print('Dual import preflight: PASS')"

  if ($LASTEXITCODE -ne 0) {
    throw "Dual import preflight failed."
  }

  Write-Host ""
  Write-Host "Running canonical Phase-boundary full suite:"
  Write-Host "  pytest -q tests"
  Write-Host ""

  pytest -q tests
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
  Write-Host "Phase 144-6 canonical final full suite: FAIL"
  exit $Code
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 144-6 canonical final full suite: PASS"
Write-Host "=============================================================="
Write-Host "Production changes in this package: none."
Write-Host "Persistent test changes in this package: none."
Write-Host "Only canonical tests/ were collected."
Write-Host "Both historical test-import styles were supported."
Write-Host "Phase 144-6 implementation/test boundary is complete."

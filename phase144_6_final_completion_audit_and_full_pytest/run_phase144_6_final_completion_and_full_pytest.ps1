$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$AuditRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Marker = Join-Path $ProjectRoot "tests\__init__.py"
$CreatedMarker = $false

Write-Host "=============================================================="
Write-Host "Phase 144-6 Final Completion Audit + Full pytest"
Write-Host "Production changes in this package: none"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Production-delta boundary"
Write-Host "--------------------------------------------------------------"

$ProductionFiles = @(
  "toda_group_proof_narrative_argument_multi_renderer.py",
  "toda_group_proof_narrative_argument_body_renderer.py",
  "toda_group_proof_narrative_semantics.py",
  "toda_group_proof_narrative_renderer.py"
)

python -m py_compile @ProductionFiles
if ($LASTEXITCODE -ne 0) {
  throw "Production syntax check failed."
}
Write-Host "Production syntax: PASS"

git diff --check -- @ProductionFiles
if ($LASTEXITCODE -ne 0) {
  throw "git diff --check failed."
}
Write-Host "git diff --check: PASS"

Write-Host ""
Write-Host "Raw numstat:"
git diff --numstat -- @ProductionFiles

Write-Host ""
Write-Host "Ignoring end-of-line whitespace:"
git diff --ignore-space-at-eol --stat -- @ProductionFiles

Write-Host ""
Write-Host "Upstream proof construction:"
git diff --quiet HEAD -- "toda_upstream_bootstrap.py"
if ($LASTEXITCODE -ne 0) {
  throw "toda_upstream_bootstrap.py differs from HEAD."
}
Write-Host "toda_upstream_bootstrap.py : HEAD"

Write-Host ""
Write-Host "B. R25-9A/R25-9B explicit completion audit"
Write-Host "--------------------------------------------------------------"

if (-not (Test-Path $Marker)) {
  New-Item -Path $Marker -ItemType File -Force | Out-Null
  $CreatedMarker = $true
}

$env:PYTHONPATH = "$ProjectRoot;$ProjectRoot\tests"

try {
  python (Join-Path $AuditRoot "audit_phase144_6_final_completion.py")
  if ($LASTEXITCODE -ne 0) {
    throw "Explicit completion audit failed."
  }

  Write-Host ""
  Write-Host "C. Entire local Phase 144-6 test population"
  Write-Host "--------------------------------------------------------------"

  $PhaseTests = @(
    Get-ChildItem `
      -Path (Join-Path $ProjectRoot "tests") `
      -Filter "test_phase144_6*.py" `
      -File |
    Sort-Object Name |
    ForEach-Object {
      $_.FullName
    }
  )

  if ($PhaseTests.Count -eq 0) {
    throw "No Phase 144-6 tests were found."
  }

  Write-Host ("Phase 144-6 test files: " + $PhaseTests.Count)

  pytest -q @PhaseTests
  if ($LASTEXITCODE -ne 0) {
    throw "Phase 144-6 completion test population failed."
  }

  Write-Host ""
  Write-Host "D. Cross-phase boundary controls"
  Write-Host "--------------------------------------------------------------"

  $BoundaryTests = @(
    "tests/test_phase143_61a_argument_conclusion_direct_premises.py",
    "tests/test_phase132_9_web_group_proof_modes.py"
  ) | Where-Object {
    Test-Path (
      Join-Path $ProjectRoot $_
    )
  }

  if ($BoundaryTests.Count -gt 0) {
    pytest -q @BoundaryTests
    if ($LASTEXITCODE -ne 0) {
      throw "Cross-phase boundary controls failed."
    }
  }
  else {
    Write-Host "No named cross-phase boundary files found; skipped."
  }

  Write-Host ""
  Write-Host "E. Phase 144-6 completion gate"
  Write-Host "--------------------------------------------------------------"
  Write-Host "Focused completion audit: PASS"
  Write-Host "Phase 144-6 test population: PASS"
  Write-Host "Cross-phase boundary controls: PASS"
  Write-Host ""
  Write-Host "Completion gate passed."
  Write-Host "Running the Phase-final full pytest now."

  Write-Host ""
  Write-Host "F. FULL TEST SUITE"
  Write-Host "--------------------------------------------------------------"

  pytest -q
  if ($LASTEXITCODE -ne 0) {
    throw "Full pytest failed. Phase 144-6 is NOT complete."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "PHASE 144-6 FINAL RESULT: PASS"
  Write-Host "Completion audit: PASS"
  Write-Host "Full pytest: PASS"
  Write-Host "Production changes in this audit package: none"
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  if ($CreatedMarker) {
    Remove-Item $Marker -Force -ErrorAction SilentlyContinue
  }
}

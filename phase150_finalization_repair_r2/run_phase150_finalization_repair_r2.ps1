$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 Finalization Repair R2"
Write-Host "Historical Narrative test-contract alignment"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$root = (Get-Location).Path
$packageDir = Join-Path $root "phase150_finalization_repair_r2"
$backupDir = Join-Path $packageDir "backup_before_r2"
$resultFile = Join-Path $packageDir "focused_pytest_r2.txt"

$testFiles = @(
  "tests/test_phase132_6_group_proof_narrative_renderer.py",
  "tests/test_phase132_7_group_proof_cli_modes.py",
  "tests/test_phase132_8_group_proof_narrative_dedup.py",
  "tests/test_phase132_9_web_group_proof_modes.py",
  "tests/test_phase133_10_sigma_label_wording.py",
  "tests/test_phase133_6_group_proof_narrative_labels.py",
  "tests/test_phase133_9_group_proof_narrative_labels.py",
  "tests/test_phase144_6_r3_production_references.py",
  "tests/test_phase144_6_r3_structured_references.py",
  "tests/test_phase144_6_r4_supporting_fact_filtering.py"
)

New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
foreach ($file in $testFiles) {
  $source = Join-Path $root $file
  if (-not (Test-Path $source)) {
    throw "Required test file not found: $file"
  }
  $dest = Join-Path $backupDir $file
  New-Item -ItemType Directory -Path (Split-Path $dest) -Force | Out-Null
  Copy-Item $source $dest -Force
}

Write-Host "A. Applying R2 test-contract updates..."
python (Join-Path $packageDir "apply_phase150_finalization_repair_r2.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "B. Syntax preflight..."
python -m py_compile @testFiles
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "C. Focused pytest only..."
$env:PYTHONPATH = $root
$env:PYTHONIOENCODING = "utf-8"
try {
  python -m pytest @testFiles -q 2>&1 | Tee-Object -FilePath $resultFile
  $pytestExit = $LASTEXITCODE
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "Focused pytest exit code: $pytestExit"
Write-Host "Result: $resultFile"
Write-Host "Full regression: NOT run"
Write-Host ""
if ($pytestExit -eq 0) {
  Write-Host "R2 focused tests PASS."
  Write-Host "Next: run the Phase 150 final full regression once."
} else {
  Write-Host "R2 still has focused failures. Do NOT run the full regression yet."
}
exit $pytestExit

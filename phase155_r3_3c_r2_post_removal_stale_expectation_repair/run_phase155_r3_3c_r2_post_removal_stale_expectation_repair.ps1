$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AuditOutput = Join-Path `
  $RepoRoot `
  "phase155_r3_3c_r2_contract_audit.json"

Write-Host "=============================================================="
Write-Host "Phase 155-R3-3C-r2 - post-removal stale expectation repair"
Write-Host "=============================================================="
Write-Host "Repository: $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing test files changed: 2"
Write-Host "Existing test functions changed: 3"
Write-Host "Import changes: none"
Write-Host "R3-3C-r1 duplicate removals are preserved."
Write-Host "Repository-wide pytest: NOT run"
Write-Host ""

Write-Host "1/4 Focused tests for the R3-3C-r2 repair tool"

python -m pytest `
  "$PackageDir\test_phase155_r3_3c_r2_tools.py" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3C-r2 tool tests failed."
}

Write-Host ""
Write-Host "2/4 Audit current runtime contract before changing expectations"

$env:PYTHONPATH = "$RepoRoot;$PackageDir"

python `
  "$PackageDir\audit_phase155_r3_3c_r2_contract.py" `
  --output "$AuditOutput"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3C-r2 runtime contract audit failed."
}

Write-Host ""
Write-Host "3/4 Apply exactly three stale expectation repairs"

python `
  "$PackageDir\apply_phase155_r3_3c_r2.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3C-r2 expectation repair failed."
}

Write-Host ""
Write-Host "4/4 Re-run only the three failures from R3-3C-r1"
Write-Host "    Previous post-removal evidence already recorded 858 other passes."

python -m pytest `
  "tests/test_phase132_9_web_group_proof_modes.py::test_phase132_9_narrative_web_adapter_preserves_math" `
  "tests/test_phase143_55b_conclusion_step_ordering.py::test_phase143_55b_pi6_3_auxiliary_order_precedes_main_order" `
  "tests/test_phase143_55b_conclusion_step_ordering.py::test_phase143_55b_pi8_5_auxiliary_order_precedes_main_order" `
  -q `
  -p no:cacheprovider

if ($LASTEXITCODE -ne 0) {
  throw "Phase 155-R3-3C-r2 repaired focused tests failed."
}

Write-Host ""
Write-Host "Phase 155-R3-3C-r2 completed."
Write-Host "Production changes: none"
Write-Host "Existing test files changed: 2"
Write-Host "Existing test functions changed: 3"
Write-Host "Prior post-removal affected verification evidence: 858 passed, 3 failed"
Write-Host "Repaired failure set: 3 passed"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "Next: Phase 155-R3-3D post-removal closure audit"

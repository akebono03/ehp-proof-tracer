$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 158-R5-3 - public Narrative single generic route"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "[1/5] Apply minimal production change"
python "$PackageDir\apply_phase158_r5_3.py"

Write-Host "[2/5] Install focused R5-3 test"
Copy-Item `
  "$PackageDir\test_phase158_r5_3_public_narrative_single_route.py" `
  ".\tests\test_phase158_r5_3_public_narrative_single_route.py" `
  -Force

Write-Host "[3/5] Syntax check"
python -m py_compile `
  ".\toda_group_proof_narrative_renderer.py" `
  ".\tests\test_phase158_r5_3_public_narrative_single_route.py"

Write-Host "[4/5] Run R5-3 focused route tests"
python -m pytest -q `
  ".\tests\test_phase158_r5_3_public_narrative_single_route.py" `
  ".\tests\test_phase143_19_method_evidence.py" `
  ".\tests\test_phase143_46_multi_argument_narrative_assembler.py"

Write-Host "[5/5] Show git diff summary"
git diff --stat -- `
  "toda_group_proof_narrative_renderer.py" `
  "tests/test_phase158_r5_3_public_narrative_single_route.py"

Write-Host ""
Write-Host "Phase 158-R5-3 focused checks completed."
Write-Host "Full pytest is intentionally NOT run; it remains for Phase 158 closure."

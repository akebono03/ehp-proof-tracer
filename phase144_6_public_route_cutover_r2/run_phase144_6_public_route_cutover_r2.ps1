$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "=============================================================="
Write-Host "Phase 144-6 Public Route Cutover R2"
Write-Host "Test import repair only"
Write-Host "=============================================================="

python "$PackageRoot\install_phase144_6_public_route_cutover_r2.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

$env:PYTHONPATH = $RepoRoot

pytest -q `
  ".\tests\test_phase144_6_public_route_cutover.py" `
  ".\tests\test_phase144_6_r5_43_11d_final_completion_audit.py" `
  ".\tests\test_phase132_7_group_proof_cli_modes.py" `
  ".\tests\test_phase132_9_web_group_proof_modes.py" `
  ".\tests\test_phase135_1_web_narrative_display_math.py" `
  ".\tests\test_phase135_2_web_narrative_inline_formatting.py" `
  ".\tests\test_phase135_3_web_narrative_readability.py"

$Code = $LASTEXITCODE
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue

if ($Code -ne 0) {
  exit $Code
}

Write-Host ""
Write-Host "Focused Public Route Cutover regression: PASS"
Write-Host "Production code changes in R2: none."
Write-Host "Full suite is intentionally NOT run."

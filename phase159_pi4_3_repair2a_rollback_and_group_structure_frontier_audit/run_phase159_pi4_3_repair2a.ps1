$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 repair2a"
Write-Host "Rollback overbroad repair2 + group-structure frontier audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/4] Roll back failed repair2"
python "$PackageRoot\apply_phase159_pi4_3_repair2a_rollback.py"
if ($LASTEXITCODE -ne 0) {
  throw "repair2a rollback failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[2/4] Compile restored production helper"
python -m py_compile `
  ".\toda_group_proof_narrative_argument_multi_renderer.py"
if ($LASTEXITCODE -ne 0) {
  throw "py_compile failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[3/4] Verify restored frontier contract"
python -m pytest `
  tests/test_phase144_6_r4_supporting_fact_filtering.py `
  tests/test_phase144_6_r25_9a_pi5_suppression.py `
  tests/test_phase144_6_r25_9a_r1_relocation_hidden.py `
  tests/test_phase143_36_argument_body_blocks.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "frontier contract regression failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[4/4] Audit ESTABLISH_GROUP_STRUCTURE second-level frontier"
python "$PackageRoot\audit_phase159_pi4_3_repair2a_group_structure_frontier.py"
if ($LASTEXITCODE -ne 0) {
  throw "group-structure frontier audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 159 pi_4^3 repair2a complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="

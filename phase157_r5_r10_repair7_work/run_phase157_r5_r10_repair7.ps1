$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157 R5-R10 repair7 - public Reference intro normalization"
Write-Host "=============================================================="

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "Repository root: $RepoRoot"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

Write-Host "Applying repair7 patch..."
python "$ScriptDir\apply_phase157_r5_r10_repair7.py"

Write-Host ""
Write-Host "Focused pytest:"
python -m pytest `
  tests/test_phase157_r5_r10_reference_proof_boundary_qed.py `
  tests/test_phase157_r5_r9_fixed_definition_body_suppression.py `
  tests/test_phase157_r5_r7_reference_definition_consequence_rendering.py `
  tests/test_phase157_r5_r6_53_bracket_definition_reference.py `
  tests/test_phase132_9_web_group_proof_modes.py `
  tests/test_phase132_7_group_proof_cli_modes.py `
  tests/test_phase150_rc4_7a_cross_group_reference_normalization.py `
  tests/test_phase144_6_r3_production_references.py `
  tests/test_phase156_r5_repair9_test_contract_after_boundary_collapse.py `
  tests/test_phase153_r11_generic_reference_attribution_filtering.py `
  tests/test_phase153_r3_4_reference_statement_rendering_connection.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "Focused pytest failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "Phase157 R5-R10 repair7 focused checks completed."
Write-Host "Low-level Reference renderer contract remains unchanged."
Write-Host "Full repository pytest is intentionally NOT run here."
Write-Host "It will be run only at Phase157 closure."

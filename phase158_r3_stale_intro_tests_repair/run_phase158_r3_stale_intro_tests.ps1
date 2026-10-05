$ErrorActionPreference = "Stop"

function Assert-LastExitCode {
  param(
    [string]$Step
  )

  if ($LASTEXITCODE -ne 0) {
    throw "$Step failed with exit code $LASTEXITCODE"
  }
}

Write-Host "=============================================================="
Write-Host "Phase 158-R3 - stale intro tests test-only repair"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $PackageDir "..")).Path

Set-Location $RepoRoot

Write-Host "[1/4] Apply test-only repair"
python `
  ".\phase158_r3_stale_intro_tests_repair\apply_phase158_r3_stale_intro_tests.py"
Assert-LastExitCode "apply test-only repair"

Write-Host "[2/4] Focused repaired tests"
python -m pytest `
  ".\tests\test_phase132_7_group_proof_cli_modes.py::test_phase132_7_group_proof_default_mode_is_narrative" `
  ".\tests\test_phase132_7_group_proof_cli_modes.py::test_phase132_7_group_proof_narrative_mode_uses_narrative_renderer" `
  ".\tests\test_phase150_rc4_7a_cross_group_reference_normalization.py::test_phase150_rc4_7a_pi10_4_numbers_normalized_references" `
  ".\tests\test_phase150_rc4_7a_cross_group_reference_normalization.py::test_phase150_rc4_7a_pi12_5_numbers_normalized_references" `
  ".\tests\test_phase150_rc4_7a_cross_group_reference_normalization.py::test_phase150_rc4_7a_pi16_9_numbers_normalized_references" `
  ".\tests\test_phase153_r3_4_reference_statement_rendering_connection.py::test_phase153_r3_4_reference_renderer_accepts_statement_lines_without_breaking_old_api" `
  ".\tests\test_phase144_6_r3_production_references.py::test_phase144_6_r3_pi6_3_generic_multi_argument_renders_reference_section" `
  ".\tests\test_phase156_r5_repair9_test_contract_after_boundary_collapse.py::test_phase156_r5_repair9_depth2_public_body_starts_after_53_boundary" `
  ".\tests\test_phase153_r11_generic_reference_attribution_filtering.py::test_phase153_r11_pi6_3_generic_section_excludes_root_self_reference" `
  -q
Assert-LastExitCode "focused repaired tests"

Write-Host "[3/4] Stale intro expectation audit"
python `
  ".\phase158_r3_stale_intro_tests_repair\audit_phase158_r3_stale_intro_tests.py"
Assert-LastExitCode "stale intro expectation audit"

Write-Host "[4/4] Re-run Phase 158-R3 112-group audit"
python `
  ".\phase158_r3_reference_intro_normalization\audit_phase158_r3.py"
Assert-LastExitCode "Phase 158-R3 112-group audit"

Write-Host "=============================================================="
Write-Host "Phase 158-R3 stale test repair complete candidate."
Write-Host "Production code changes: none"
Write-Host "Full repository pytest: NOT run"
Write-Host "=============================================================="

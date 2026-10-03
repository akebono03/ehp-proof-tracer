$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R5-R6 repair2 - fixed component union selection"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "Repository root: $RepoRoot"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

python "$PackageDir\apply_phase157_r5_r6_repair2.py"

Write-Host ""
Write-Host "Focused lightweight pytest only:"

python -m pytest `
  tests/test_phase157_r5_r6_53_bracket_definition_reference.py `
  tests/test_phase157_r5_r4_generic_reference_selection.py `
  tests/test_phase157_r5_r3_boundary_catalog_expansion.py `
  tests/test_phase157_r4_r2_boundary_catalog.py `
  tests/test_phase157_r2_literature_statement_boundary.py `
  tests/test_phase156_r5_reference_attribution_separation.py `
  tests/test_phase156_r5_repair2_lemma52_specialization_attribution.py `
  tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py `
  tests/test_phase58_nu_prime_specialization.py `
  tests/test_phase58_lemma52_specialization.py `
  -q

Write-Host ""
Write-Host "Phase157-R5-R6 repair2 focused verification complete."
Write-Host "112-group cross-audit is deferred until R5-R6 focused PASS."
Write-Host "Repository-wide pytest remains deferred to Phase157 closure."

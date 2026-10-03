$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R5-R7 - Reference definition/consequence rendering"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "Repository root: $RepoRoot"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

python "$PackageDir\apply_phase157_r5_r7.py"

Write-Host ""
Write-Host "Focused lightweight pytest only:"

python -m pytest `
  tests/test_phase157_r5_r7_reference_definition_consequence_rendering.py `
  tests/test_phase157_r5_r6_53_bracket_definition_reference.py `
  tests/test_phase157_r5_r4_generic_reference_selection.py `
  tests/test_phase157_r2_literature_statement_boundary.py `
  tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py `
  -q

Write-Host ""
Write-Host "Phase157-R5-R7 focused verification complete."
Write-Host "112-group cross-audit remains next after PASS."
Write-Host "Repository-wide pytest remains deferred to Phase157 closure."

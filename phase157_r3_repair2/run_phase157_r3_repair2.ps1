$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R3 repair2 - robust Reference retention + body restore"
Write-Host "=============================================================="
Write-Host "Repository root: $PWD"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

python ".\phase157_r3_repair2\apply_phase157_r3_repair2.py"

Write-Host ""
Write-Host "Focused pytest only:"
python -m pytest `
  tests/test_phase157_r2_literature_statement_boundary.py `
  tests/test_phase157_r3_pi6_3_reference_boundary.py `
  tests/test_phase153_r5_reference_selection.py `
  tests/test_phase156_r5_repair9_test_contract_after_boundary_collapse.py `
  -q

Write-Host ""
Write-Host "Phase157-R3 repair2 focused verification complete."
Write-Host "Repository-wide pytest is intentionally deferred to Phase157 closure."

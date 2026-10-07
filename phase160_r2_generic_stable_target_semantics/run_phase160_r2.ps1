$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 160-R2 generic stable target / canonical base semantics"
Write-Host "=============================================================="
Write-Host "Repository root: $(Get-Location)"
Write-Host ""

Write-Host "[1/2] Apply Phase 160-R2"
python ".\phase160_r2_generic_stable_target_semantics\apply_phase160_r2.py"

Write-Host ""
Write-Host "[2/2] Run focused tests only"
python -m pytest -q `
  "tests/test_phase160_stable_target_semantics.py" `
  "tests/test_stable_rules.py"

Write-Host ""
Write-Host "Phase 160-R2 focused verification completed."
Write-Host "No full test suite was run."

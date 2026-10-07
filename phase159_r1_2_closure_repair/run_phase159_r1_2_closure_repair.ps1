$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159-R1-2 closure repair"
Write-Host "=============================================================="
Write-Host "Repository root: $(Get-Location)"

Write-Host ""
Write-Host "[1/5] Apply minimal closure repair"
python ".\phase159_r1_2_closure_repair\apply_phase159_r1_2_closure_repair.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[2/5] Run pi3^2 focused tests"
python -m pytest -q ".\tests\test_phase159_r1_2_pi3_2_closure.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[3/5] Run generic dependency regression"
python -m pytest -q ".\tests\test_phase157_r20_generic_dependency_rendering.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[4/5] Run public generic route regression"
python -m pytest -q ".\tests\test_phase158_r5_5b_public_generic_order_route.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "[5/5] git diff --check"
git diff --check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 159-R1-2 closure repair verification PASS"
Write-Host "Full pytest intentionally NOT run."
Write-Host "=============================================================="

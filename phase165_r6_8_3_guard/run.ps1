$ErrorActionPreference = 'Stop'
$root = (Resolve-Path '.').Path
if (-not (Test-Path (Join-Path $root 'phase165_r55_nk_only_goal.py'))) {
  throw 'Run this from the ehp_proof repository root.'
}
python -m pytest -q '.\phase165_r6_8_3_guard\tests\test_phase165_r6_8_3_contract.py'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R6-8(3) contract PASS; full pytest NOT run'

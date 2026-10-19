$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
python ".\phase165_r6_8_3_stage1\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q ".\phase165_r6_8_3_guard\tests\test_phase165_r6_8_3_contract.py" -k "phase53 or phase54"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Stage1 source guards PASS; Phase55 NOT migrated; no full pytest run'

python -m pytest -q ".\phase165_r6_8_3_stage1\tests\test_phase165_r6_8_3_stage1.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Stage1 mathematical checks PASS; Phase55 remains pending"

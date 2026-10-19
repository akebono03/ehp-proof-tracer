$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
python ".\phase165_r6_8_3_stage1_import_fix\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q ".\phase165_r6_8_3_stage1_import_fix\tests\test_phase165_r6_8_3_stage1_import_fix.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R6-8(3) Stage1 import targeted PASS; Phase55 NOT migrated; full pytest NOT run"

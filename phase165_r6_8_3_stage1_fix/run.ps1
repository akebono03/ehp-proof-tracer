$ErrorActionPreference = 'Stop'
cd (Split-Path -Parent $PSScriptRoot)
python ".\phase165_r6_8_3_stage1_fix\apply.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q ".\phase165_r6_8_3_stage1_fix\tests\test_phase165_r6_8_3_stage1_fix.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Stage1 fix targeted PASS; Phase 55 pending; full pytest NOT run'

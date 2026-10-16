$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\phase165_r52_r9_shared_math.py')) { throw 'Run from the project root.' }
if (-not (Test-Path '.\phase165_r6_2_unified_registry_r3\r3_inventory.py')) { throw 'R3 inventory package is required.' }
python -m pytest -q .\phase165_r6_2_unified_registry_r3_r2\test_r3_r2_audit.py
if ($LASTEXITCODE -ne 0) { throw 'R3-2 targeted tests failed.' }
python -m phase165_r6_2_unified_registry_r3_r2.r3_r2_audit --root . --output .\phase165_r6_2_unified_registry_r3_r2\reports
if ($LASTEXITCODE -ne 0) { throw 'R3-2 audit failed.' }
Write-Output 'R3-2 static mapping complete; production files unchanged; full pytest NOT run.'

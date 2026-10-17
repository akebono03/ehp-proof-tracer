$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\phase165_r52_r9_shared_math.py')) { throw 'Run from repository root.' }
if (-not (Test-Path '.\phase165_r6_2_unified_registry_r1\unified_backward_rule_registry.py')) { throw 'R1 must be installed.' }
python -m pytest -q .\phase165_r6_2_unified_registry_r3\test_r3_inventory.py
if ($LASTEXITCODE -ne 0) { throw 'R3 targeted tests failed.' }
python .\phase165_r6_2_unified_registry_r3\r3_inventory.py --root . --output .\phase165_r6_2_unified_registry_r3\reports
if ($LASTEXITCODE -ne 0) { throw 'R3 audit failed.' }
Write-Output 'R3 source inventory completed; production files unchanged; full pytest NOT run.'

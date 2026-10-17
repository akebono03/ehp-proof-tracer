$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\phase165_r8_rule_provider.py')) { throw 'Run from repository root.' }
if (-not (Test-Path '.\phase165_r6_2_unified_registry_r1\unified_backward_rule_registry.py')) { throw 'R1 must be installed.' }
python -m pytest -q .\phase165_r6_2_unified_registry_r2\test_r2_audit.py
if ($LASTEXITCODE -ne 0) { throw 'R2 targeted tests failed.' }
python .\phase165_r6_2_unified_registry_r2\r2_audit.py --root . --output .\phase165_r6_2_unified_registry_r2\reports
if ($LASTEXITCODE -ne 0) { throw 'R2 audit failed.' }
Write-Output 'R2 read-only audit completed; production files unchanged; full pytest NOT run.'
